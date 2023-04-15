from django.urls import path
from baykeshop.module.payment import views

from baykeshop.module.payment.alipay.notify import AlipayNotifyView

urlpatterns = [
    path('confirm/', views.ConfirmOrderAPIView.as_view(), name='confirm'),
    path("notify/", AlipayNotifyView.as_view(), name='alipay_notify')
]