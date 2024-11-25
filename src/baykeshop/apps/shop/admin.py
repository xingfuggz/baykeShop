from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *
from baykeshop.site.admin import site as bayke_site


class BaykeShopSpecValueInline(admin.TabularInline):
    extra = 1
    model = BaykeShopSpecValue


class BaykeShopSpecValueCombinationInline(admin.TabularInline):
    extra = 1
    model = BaykeShopSpecValueCombination


class BaykeShopSKUInline(admin.TabularInline):
    extra = 1
    model = BaykeShopSKU


class BaykeShopSPUGalleryInline(admin.TabularInline):
    extra = 1
    model = BaykeShopSPUGallery


class BaykeShopCategoryInline(admin.TabularInline):
    extra = 1
    model = BaykeShopCategory
    fields = ('name', 'icon', 'sort',)


@admin.register(BaykeShopCategory, site=bayke_site)
class BaykeShopCategoryAdmin(admin.ModelAdmin):
    """ 商品分类 """
    list_display = ('id', 'name', 'is_floor', 'is_nav', 'create_time')
    list_editable = ('is_floor', 'is_nav')
    list_filter = ('is_floor', 'is_nav')
    list_display_links = ('id', 'name')
    readonly_fields = ('pid',)
    inlines = [BaykeShopCategoryInline,]

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(pid__isnull=False)


@admin.register(BaykeShopBrand, site=bayke_site)
class BaykeShopBrandAdmin(admin.ModelAdmin):
    '''Admin View for BaykeShopBrand'''

    list_display = ('id', 'name', 'create_time')
    list_display_links = ('id', 'name')


@admin.register(BaykeShopSpec, site=bayke_site)
class BaykeShopSpecAdmin(admin.ModelAdmin):
    '''Admin View for BaykeShopSpec'''

    list_display = ('id', 'name', 'create_time')
    inlines = [BaykeShopSpecValueInline,]


@admin.register(BaykeShopSPU, site=bayke_site)
class BaykeShopSPUModelAdmin(admin.ModelAdmin):
    '''Admin View for BaykeShopSPU'''

    list_display = ('id', 'name', 'brand', 'category', 'create_time')
    list_display_links = ('id', 'name')
    inlines = [BaykeShopSKUInline, BaykeShopSPUGalleryInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'brand', 'category', 'image',  )
        }),
        (_('SEO及详情'), {
            'classes': ('collapse',),
            'fields': ('keywords', 'description', 'content',)
        }),
        (_('SPU属性'), {
            'classes': ('collapse',),
            'fields': ('is_boutique', 'is_new', 'is_recommend', 'is_on_sale')
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 商品分类仅支持选择二级分类
        if db_field.name == 'category':
            kwargs['queryset'] = BaykeShopCategory.objects.filter(pid__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BaykeShopSpecValueCombination, site=bayke_site)
class BaykeShopSpecValueCombinationModelAdmin(admin.ModelAdmin):
    '''Admin View for BaykeShopSpecValueCombination'''

    list_display = ('id', 'create_time')
    list_display_links = ('id',)
    filter_horizontal = ("specs", )


@admin.register(BaykeShopGallery, site=bayke_site)
class BaykeShopGalleryModelAdmin(admin.ModelAdmin):
    '''Admin View for BaykeShopGallery'''

    list_display = ('id', 'image', 'desc', 'target', 'create_time')
    list_display_links = ('id', 'desc', 'image')
    list_filter = ('is_show',)