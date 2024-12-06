from django.urls import path, include


urlpatterns = [
    path('', include('baykeshop.contrib.shop.urls')),
    path('member/', include('baykeshop.contrib.member.urls')),
    path('article/', include('baykeshop.contrib.article.urls')),
    # 接口url
    path('api/', include('baykeshop.api.urls', namespace='baykeshop_api')),
]