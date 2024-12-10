from django.urls import path, re_path

from . import views

app_name = 'shop'

urlpatterns = [
    # 支付宝支付回调(必须在第一个)
    path('pay/callback/', views.AlipayCallbackView.as_view(), name='alipay-callback'),   
    # 商品列表
    path('list/', views.BaykeShopGoodsListView.as_view(), name='list'),
    # 搜索
    path('search/', views.BaykeShopSearchView.as_view(), name='search'),
    # 商品详情
    path('detail/<int:pk>/', views.BaykeShopGoodsDetailView.as_view(), name='detail'),
    # 商品分类
    path('category/<int:pk>/', views.BaykeShopCategoryListView.as_view(), name='category'),
    # 购物车
    path('carts/', views.BaykeShopCartsListView.as_view(), name='carts'),
    # 商品结算页面
    re_path(r'^list/(?P<skuid>\d+)/(?P<num>\d+)/$', views.BaykeShopCashView.as_view(), name='cash-sku'),
    # 购物车结算页面
    re_path(r'^carts/(?P<skuids>\d+(?:,\d+)*)/$', views.BaykeShopCashView.as_view(), name='cash_cartids'),
    # 支付页面
    path('pay/<slug:order_sn>/', views.BaykeShopOrdersPayView.as_view(), name='orders-pay'),
    # 首页
    path('', views.BaykeShopIndexView.as_view(), name='index'),
]