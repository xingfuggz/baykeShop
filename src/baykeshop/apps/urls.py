from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from baykeshop.apps.article.models import BaykeArticle, BaykeArticleCategory, BaykeArticleTags
from baykeshop.apps.shop.models import BaykeShopCategory, BaykeShopSPU, BaykeShopBrand
# app_name = 'baykeshop_app'

urlpatterns = [
    # path('', include('baykeshop.apps.core.urls')),
    path('', include('baykeshop.apps.shop.urls', namespace='shop')),
    path('article/', include('baykeshop.apps.article.urls', namespace='article')),
    path('user/', include('baykeshop.apps.user.urls', namespace='user')),
    path('order/', include('baykeshop.apps.order.urls', namespace='order')),
    path('core/', include('baykeshop.apps.core.urls', namespace='core')),
    path(
        "sitemap.xml", sitemap,
        {"sitemaps": {
            "article": GenericSitemap({
                "queryset": BaykeArticle.objects.filter(is_show=True),
                "priority": 0.6,
                "changefreq": "daily"
            }, priority=0.6),
            "article_category": GenericSitemap({
                "queryset": BaykeArticleCategory.objects.filter(is_show=True),
                "priority": 0.6,
                "changefreq": "daily"
            }, priority=0.6),
            "article_tags": GenericSitemap({
                "queryset": BaykeArticleTags.objects.all(),
                "priority": 0.6,
                "changefreq": "daily"
            }, priority=0.6),
            "shop_category": GenericSitemap({
                "queryset": BaykeShopCategory.objects.all(),
                "priority": 0.6,
                "changefreq": "daily"
            }, priority=0.6),
            "shop_spu": GenericSitemap({
                "queryset": BaykeShopSPU.objects.all(),
                "priority": 0.6,
                "changefreq": "daily"
            }, priority=0.6),
            "shop_brand": GenericSitemap({
                "queryset": BaykeShopBrand.objects.all(),
                "priority": 0.6,
                "changefreq": "daily"
            }, priority=0.6),
        }},
        name="sitemap",
    )
]

