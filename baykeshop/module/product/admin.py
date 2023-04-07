from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from baykeshop.public.sites import bayke_site
from baykeshop.module.product.models import BaykeCategory, BaykeGoods, BaykeProduct
from baykeshop.module.admin.options import BaseModelAdmin, TabularInline, StackedInline


class BaykeCategoryInline(StackedInline):
    model = BaykeCategory
    min_num = 1
    max_num = 20
    extra = 1
    # exclude = ('site', )
    # raw_id_fields = (,)
    
    
class BaykeProductInline(TabularInline):
    model = BaykeProduct
    # min_num = 1
    max_num = 20
    extra = 1
    can_delete = False



@admin.register(BaykeCategory, site=bayke_site)
class BaykeShopCategoryAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'parent', 'operate')
    exclude = ('parent', )
    inlines = (BaykeCategoryInline, )
    # search_fields = ('parent__name',)
    # autocomplete_fields = ('parent', )
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = BaykeCategory.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BaykeGoods, site=bayke_site)
class BaykeGoodsAdmin(BaseModelAdmin):
    list_display = (
        'id', 
        'dis_cover_pic', 
        'title', 
        'dis_price', 
        'dis_spec', 
        'dis_sales',
        'dis_stock',
        'operate'
    )
    list_display_links = ('title', )
    filter_horizontal = ('categorys',)
    # form = BaykeShopSPUForm
    inlines = (BaykeProductInline, )
    
    class Media:
        css = {'all': ['baykeadmin/css/ordersku.css']}
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'categorys':
            kwargs['queryset'] = BaykeCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_skus(self, obj):
        return obj.baykeproduct_set.order_by('price')
    
    @admin.display(description="封面图")
    def dis_cover_pic(self, obj):
        return format_html(mark_safe("<img width='64px' height='64px' src='{}' />"), obj.pic.url)
    
    @admin.display(description="价格")
    def dis_price(self, obj):
        return self.get_skus(obj).first().price
    
    @admin.display(description="包含规格")
    def dis_spec(self, obj):
        return format_html_join(
            '\n', '{}<br>',
            (   
               (f"{k['spec__name']}:{k['name']}" for k in u.options.values('spec__name','name',)) for u in self.get_skus(obj) if u.options.exists() 
            )
        )
    
    @admin.display(description="销量")
    def dis_sales(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('sales'))['sales__sum']

    @admin.display(description="库存")
    def dis_stock(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('stock'))['stock__sum']