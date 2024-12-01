from django.urls import path, include


urlpatterns = [
    path('shop/', include('baykeshop.contrib.shop.urls')),
    path('member/', include('baykeshop.contrib.member.urls')),
    # 接口url
    path('api/', include('baykeshop.api.urls', namespace='baykeshop_api')),
]