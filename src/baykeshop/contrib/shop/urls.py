from django.urls import path, re_path

from . import views

app_name = 'shop'

urlpatterns = [
    path('list/', views.BaykeShopGoodsListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.BaykeShopGoodsDetailView.as_view(), name='detail'),
    path('category/<int:pk>/', views.BaykeShopCategoryListView.as_view(), name='category'),
    path('carts/', views.BaykeShopCartsListView.as_view(), name='carts'),
    re_path(r'^list/(?P<skuid>\d+)/(?P<num>\d+)/$', views.BaykeShopCashView.as_view(), name='cash-sku'),
    re_path(r'^carts/(?P<skuids>\d+(?:,\d+)*)/$', views.BaykeShopCashView.as_view(), name='cash_cartids'),
    path('pay/<slug:order_sn>/', views.BaykeShopOrdersPayView.as_view(), name='orders-pay'),
    path('pay/callback/', views.AlipayCallbackView.as_view(), name='alipay-callback'),
]