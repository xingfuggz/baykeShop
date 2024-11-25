from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.BaykeShopIndexView.as_view(), name='index'),
    path('spu/', views.BaykeShopSPUListView.as_view(), name='spu-list'),
    path('category/<int:pk>/spu/', views.BaykeShopCategorySPUListView.as_view(), name='category-spu-list'),
    path('spu/<int:pk>/', views.BaykeShopSPUDetailView.as_view(), name='spu-detail'),
    path('cart/', views.BaykeShopCartListView.as_view(), name='cart-list'),
    path('cart/add/', views.BaykeShopCartAddView.as_view(), name='cart-add'),
    path('cart/change/', views.BaykeShopCartChangeView.as_view(), name='cart-change'),
    path('cart/del/', views.BaykeShopCartDelView.as_view(), name='cart-del'),
]