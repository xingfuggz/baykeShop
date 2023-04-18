from django.contrib import admin
from django.utils.html import format_html

from baykeshop.module.admin.options import BaseModelAdmin

from baykeshop.public.sites import bayke_site
from baykeshop.public.models import BaykeBanner
from baykeshop.module.product import admin as product_admin
from baykeshop.module.user import admin as user_admin
from baykeshop.module.order import admin as order_admin
from baykeshop.module.article import admin as article_admin
from baykeshop.module.comment import admin as comment_admin


@admin.register(BaykeBanner, site=bayke_site)
class BaykeShopBannerAdmin(BaseModelAdmin):
    list_display = ('id', 'imgformat', 'target_url', 'operate')
    
    @admin.display(description="轮播图")
    def imgformat(self, obj):
        return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')

    class Media:
        css = {'all': ['baykeadmin/css/ordersku.css']}
        

