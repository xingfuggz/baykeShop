import json
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from django.template.loader import render_to_string

# Register your models here.
from baykeshop.sites import admin as bayke_admin
from .forms import BaykeShopGoodsSKUForm
from .models import *


class BaykeShopCategoryInline(bayke_admin.TabularInline):
    model = BaykeShopCategory
    extra = 1


@admin.register(BaykeShopCategory)
class BaykeShopCategoryAdmin(bayke_admin.ModelAdmin):
    list_display = ["name", "parent", "order", "is_floor", "is_nav", "is_show"]
    list_editable = ["order", "is_show"]
    list_filter = [
        "is_show",
    ]
    search_fields = ["name"]
    readonly_fields = ["parent"]
    inlines = [BaykeShopCategoryInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "icon",
                    "order",
                    "is_floor",
                    "is_nav",
                    "is_show",
                )
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = BaykeShopCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_inline_instances(self, request, obj=None):
        if obj and obj.parent:
            return []
        return super().get_inline_instances(request, obj)


class BaykeShopGoodsSKUInline(bayke_admin.StackedInline):
    model = BaykeShopGoodsSKU
    extra = 1
    form = BaykeShopGoodsSKUForm
    readonly_fields = ("sales",)


class BaykeShopGoodsImagesInline(bayke_admin.TabularInline):
    model = BaykeShopGoodsImages
    extra = 1


@admin.register(BaykeShopGoods)
class BaykeShopGoodsAdmin(bayke_admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
        "brand",
        "price",
        "sales",
        "stock",
        "is_recommend",
        "created_time",
    )
    list_display_links = ("id", "name", "image")
    list_editable = ("is_recommend",)
    list_filter = ("category", "brand")
    search_fields = ("name", "category__name", "brand__name")
    inlines = [BaykeShopGoodsSKUInline, BaykeShopGoodsImagesInline]
    fieldsets = (
        (
            _("基本信息"),
            {
                "fields": (
                    "name",
                    "category",
                    "brand",
                )
            },
        ),
        (
            _("商品详情"),
            {
                # 'classes': ('collapse',),
                "fields": (
                    "keywords",
                    "description",
                    "detail",
                )
            },
        ),
    )
    filter_horizontal = ("category",)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = BaykeShopCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    @admin.display(description="商品价格")
    def price(self, obj):
        if obj.price:
            return round(obj.price, 2)
        return None

    @admin.display(description="商品销量")
    def sales(self, obj):
        return obj.sales

    @admin.display(description="商品库存")
    def stock(self, obj):
        return obj.stock

    @admin.display(description="商品图片")
    def image(self, obj):
        return format_html(
            '<img src="/media/{}" width="64" height="64" />', obj.image_url
        )

    def save_formset(self, request, form, formset, change):
        if formset.model == BaykeShopGoodsSKU:
            for _form in formset:
                if not _form.cleaned_data:
                    print(_form.instance, _form.cleaned_data)
                    self.message_user(
                        request,
                        f"【{_form.instance}】的商品规格未设置，请设置后再保存，至少包含一个SKU！",
                        level="ERROR",
                    )
                    break
        if formset.model == BaykeShopGoodsImages:
            for _form in formset:
                if not _form.cleaned_data:
                    self.message_user(
                        request,
                        f"【{_form.instance}】的商品图片未设置，请设置后再保存，至少包含一张图片！",
                        level="ERROR",
                    )
                    break
        return super().save_formset(request, form, formset, change)


@admin.register(BaykeShopBrand)
class BaykeShopBrandAdmin(bayke_admin.ModelAdmin):
    """Admin View for BaykeShopBrand"""

    list_display = ("id", "name", "image", "order", "created_time")
    list_display_links = ("id", "name")
    search_fields = ("name", "description")
    list_editable = ("order",)

    fieldsets = (
        (_("基本信息"), {"fields": ("image", "name", "description", "order")}),
    )


class BaykeShopOrdersGoodsInline(bayke_admin.TabularInline):
    model = BaykeShopOrdersGoods
    extra = 0
    exclude = ("specs", "sku", "detail", "image")
    readonly_fields = ("_image", "name", "price", "quantity", "_specs", "sku_sn")

    @admin.display(description="规格")
    def _specs(self, obj):
        specs = obj.specs
        if isinstance(specs, str):
            specs = json.loads(obj.specs)
        if not specs:
            return "-"
        return ", ".join([f"{spec['parent__name']}:{spec['name']}" for spec in specs])

    @admin.display(description="商品图片")
    def _image(self, obj):
        if not obj.image:
            return "-"
        return format_html('<img src="/media/{}" width="64" height="64" />', obj.image)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(BaykeShopOrders)
class BaykeShopOrdersAdmin(bayke_admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "order_sn",
        "order_skus",
        "status",
        "pay_type",
        "pay_price",
        "is_verify",
        "is_comment",
        "created_time",
        "pay_time",
    )
    list_display_links = ("id", "user", "order_sn")
    search_fields = ("id", "user__username", "user__nickname")
    list_filter = ("status", "pay_type", "is_verify", "is_comment")
    readonly_fields = (
        "order_sn",
        "user",
        "pay_type",
        "is_comment",
        "pay_sn",
        "pay_time",
        "is_verify",
        "verify_time",
    )
    inlines = [
        BaykeShopOrdersGoodsInline,
    ]
    actions = ["shipments", "verify"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # 未支付和未发货订单可操作修改
        if obj and obj.status in [0]:
            return super().has_change_permission(request, obj)
        return False

    @admin.display(description="订单商品")
    def order_skus(self, obj):
        queryset = obj.baykeshopordersgoods_set.all()
        return render_to_string(
            "baykeshop/admin/ordersgoods.html", {"queryset": queryset}
        )

    @admin.action(description="所选订单 发货")
    def shipments(self, request, queryset):
        for item in queryset:
            if item.status != BaykeShopOrders.OrderStatus.PAID:
                continue
            item.status = BaykeShopOrders.OrderStatus.SHIPPED
            item.save()
        self.message_user(request, "发货成功")

    @admin.action(description="所选订单 核销")
    def verify(self, request, queryset):
        for item in queryset:
            if item.status != BaykeShopOrders.OrderStatus.VERIFY:
                continue
            item.status = BaykeShopOrders.OrderStatus.SIGNED
            item.is_verify = True
            item.pay_time = timezone.now()
            item.save()
        self.message_user(request, "核销成功")


# 规格值
class BaykeShopSpecInline(bayke_admin.TabularInline):
    model = BaykeShopSpec
    extra = 1
    verbose_name = _("规格值")
    verbose_name_plural = _("规格值")


@admin.register(BaykeShopSpec)
class BaykeShopSpecAdmin(bayke_admin.ModelAdmin):
    """Admin View for BaykeShopSpec"""

    list_display = ("id", "name", "parent", "order", "is_show", "created_time")
    list_display_links = ("id", "name")
    search_fields = ("name",)

    fieldsets = ((_("规格名称"), {"fields": ("name", "order", "is_show")}),)
    readonly_fields = ("parent",)
    inlines = [BaykeShopSpecInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = BaykeShopSpec.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_inline_instances(self, request, obj=None):
        if obj and obj.parent:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(BaykeShopOrdersComment)
class BaykeShopOrdersCommentAdmin(bayke_admin.ModelAdmin):
    """Admin View for BaykeShopOrdersComment"""

    list_display = (
        "id",
        "user",
        "order",
        "score",
        "content",
        "reply_user",
        "status",
        "created_time",
    )
    list_display_links = ("id", "user", "order")
    list_editable = ("status",)
    search_fields = ("user__username", "user__nickname")
    list_filter = ("score",)
    readonly_fields = ("user", "order", "content", "reply_user", "score")

    fieldsets = (
        (_("评论信息"), {"fields": ("user", "order", "content", "score")}),
        (_("回复信息"), {"fields": ("reply_user", "reply_content", "status")}),
    )

    def save_model(self, request, obj, form, change):
        obj.reply_user = request.user
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return False
