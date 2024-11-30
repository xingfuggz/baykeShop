from django.urls import path, include


urlpatterns = [
    path('shop/', include('baykeshop.contrib.shop.urls')),
]