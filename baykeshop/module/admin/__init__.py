from django.contrib import admin
from django.utils.html import format_html

from baykeshop.module.admin.options import BaseModelAdmin

from baykeshop.public.sites import bayke_site
from baykeshop.public.models import BaykeBanner
from baykeshop.module.product import models as product



@admin.register(BaykeBanner, site=bayke_site)
class BaykeShopBannerAdmin(BaseModelAdmin):
    list_display = ('id', 'imgformat', 'target_url', 'operate')
    
    @admin.display(description="轮播图")
    def imgformat(self, obj):
        return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')

    class Media:
        css = {'all': ['baykeadmin/css/ordersku.css']}
        
bayke_site.register(product.BaykeCategory)
