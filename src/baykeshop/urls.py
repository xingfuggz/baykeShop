from django.urls import path, include



urlpatterns = [
    path('member/', include('baykeshop.contrib.member.urls')),
    path('article/', include('baykeshop.contrib.article.urls')),
    path('', include('baykeshop.contrib.shop.urls')),
    # 接口url
    path('api/', include('baykeshop.api.urls', namespace='baykeshop_api')),
]