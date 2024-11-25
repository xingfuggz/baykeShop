from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    # 订单列表
    path('list/', views.OrderListView.as_view(), name='order-list'),
    # 订单详情
    path('detail/<slug:order_sn>/', views.OrderDetailView.as_view(), name='order-detail'),
    # 收银台
    path('cash/', views.CashRegisterView.as_view(), name='order-cash'),
    # 创建订单
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    # 支付页面
    path('pay/<slug:order_sn>/', views.OrderPayView.as_view(), name='order-pay'),
    # 支付宝回调
    path('alipay/', views.AlipayCallbackView.as_view(), name='order-alipay'),
    # 订单状态操作，确认收货 
    path('action/<slug:order_sn>/', views.OrderStatusActionView.as_view(), name='order-action'),
    # 评价
    path('comment/<slug:order_sn>/', views.CommentActionView.as_view(), name='order-comment'),
]