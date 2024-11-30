from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('list/', views.BaykeShopGoodsListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.BaykeShopGoodsDetailView.as_view(), name='detail'),
    path('category/<int:pk>/', views.BaykeShopCategoryListView.as_view(), name='category'),
]