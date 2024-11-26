from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from baykeshop.sites import admin as bayke_admin

from .models import *

admin.site.register([BaykeShopOrdersGoods])


class BaykeShopCategoryInline(admin.TabularInline):
    model = BaykeShopCategory
    extra = 1


@admin.register(BaykeShopCategory)
class BaykeShopCategoryAdmin(bayke_admin.ModelAdmin):
    list_display = ['name', 'parent', 'order', 'is_show']
    list_editable = ['order', 'is_show']
    list_filter = ['is_show',]
    search_fields = ['name']
    readonly_fields = ['parent']
    inlines = [BaykeShopCategoryInline]

    fieldsets = (
        (None, {
            'fields': (
                'name', 'icon', 'parent', 'order', 'is_show', 
            )
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = BaykeShopCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_inline_instances(self, request, obj=None):
        if obj.parent:
            return []
        return super().get_inline_instances(request, obj)


class BaykeShopGoodsSKUInline(admin.TabularInline):
    model = BaykeShopGoodsSKU
    extra = 1


@admin.register(BaykeShopGoods)
class BaykeShopGoodsAdmin(bayke_admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'brand', 'created_time', 'updated_time')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'category__name', 'brand__name')
    inlines = [
        BaykeShopGoodsSKUInline,
        # BaykeShopGoodsSpecificationAdmin,
        # BaykeShopGoodsImageAdmin,
    ]
    fieldsets = (
        (_('基本信息'), {
            'fields': ('name', 'category', 'brand', 'image', 'images', 'is_multi',)
        }),
        (_('商品详情'), {
            'fields': ('keywords', 'description', 'detail',)
        }),
    )


@admin.register(BaykeShopBrand)
class BaykeShopBrandAdmin(bayke_admin.ModelAdmin):
    '''Admin View for BaykeShopBrand'''
    list_display = ('id', 'name', 'image', 'order', 'created_time')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('order',)

    fieldsets = (
        (_('基本信息'), {
            'fields': ('image', 'name', 'description', 'order')
        }),
    )


class BaykeShopOrdersGoodsInline(bayke_admin.TabularInline):
    model = BaykeShopOrdersGoods
    extra = 0
    readonly_fields = (
        'sku_sn', 'sku', 'name', 'price', 'quantity', 'detail', 'image', 'specs'
    )


@admin.register(BaykeShopOrders)
class BaykeShopOrdersAdmin(bayke_admin.ModelAdmin):
    list_display = (
        'id', 'user', 'order_sn', 'status', 'pay_type', 
        'total_price', 'pay_price', 'is_verify', 'is_comment',
        'created_time', 'pay_time'
    )
    list_display_links = ('id', 'user', 'order_sn')
    search_fields = ('id', 'user__username', 'user__nickname')
    list_filter = ('status', 'pay_type', 'is_verify', 'is_comment')
    readonly_fields = (
        'order_sn', 'total_price', 'user', 'pay_type', 'is_comment',
        'pay_sn', 'pay_time', 'is_verify', 'verify_time'
    )
    inlines = [
        BaykeShopOrdersGoodsInline,
    ]
    fieldsets = (
        (_('订单信息'), {
            'fields': ('order_sn', 'user', 'status', 'pay_type', 'total_price', 'pay_price', 'is_comment')
        }),
        (_('支付信息'), {
            'fields': ('pay_sn', 'pay_time')
        }),
        (_('核销信息'), {
            'fields': ('is_verify', 'verify_time',)
        }),
        (_('收货信息'), {
            'fields': ('address', 'phone','receiver')
        })
    )

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        # 未支付和未发货订单可操作修改
        if obj and obj.status in [0, 1]:
            return super().has_change_permission(request, obj)
        return False
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        # 已支付订单不能再修改支付金额
        if obj and obj.status >= BaykeShopOrders.ORDER_STATUS.SHIPPED:
            readonly_fields = list(readonly_fields) + ['pay_price',]
        return readonly_fields