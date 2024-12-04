from datetime import timedelta
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from rest_framework import serializers

from baykeshop.contrib.shop.models import BaykeShopOrders
from baykeshop.payment import alipay as alipay_sdk

class BaykeShopOrdersPaySerializer(serializers.ModelSerializer):

    pay_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BaykeShopOrders
        fields = ('pay_type', 'pay_url')

    def validate_pay_type(self, value):
        if value == BaykeShopOrders.PayType.WECHATPAY:
            messages.error(self.context['request'], _('暂不支持微信支付'))
            raise serializers.ValidationError(_('暂不支持微信支付'))
        if self.instance.status != BaykeShopOrders.OrderStatus.UNPAID:
            messages.error(self.context['request'], _('订单状态错误'))
            raise serializers.ValidationError(_('该状态下的订单无法支付, 请联系客服'))
        return value

    def update(self, instance, validated_data):

        # 判断订单创建时间是否在一个小时之内,超时则不能再支付了
        if (timezone.now() - instance.created_time) > timedelta(hours=1):
            instance.status = BaykeShopOrders.OrderStatus.EXPIRED
            instance.save()
            messages.error(self.context['request'], _('订单已超时, 请重新下单'))
            raise serializers.ValidationError(_('订单已过期'))
        
        pay_type = validated_data.get('pay_type')
        if pay_type == BaykeShopOrders.PayType.ALIPAY:
            instance.pay_type = BaykeShopOrders.PayType.ALIPAY
        elif pay_type == BaykeShopOrders.PayType.CASH:
            instance.pay_type = BaykeShopOrders.PayType.CASH
            instance.pay_sn = instance.order_sn
            instance.is_verify = True
            instance.status = BaykeShopOrders.OrderStatus.VERIFY
        instance.save()
        return instance

    def get_pay_url(self, instance):
        """获取支付链接"""
        url = ''
        # 支付宝回调地址
        callback_url=self.context['request'].build_absolute_uri(reverse('shop:alipay-callback')),
        if instance.pay_type == BaykeShopOrders.PayType.CASH:
            messages.success(self.context['request'], _('订单已提交，核销中...'))
            return reverse('member:orders-detail', kwargs={'order_sn': instance.order_sn})
        try:
            url = alipay_sdk.page_pay(
                order_sn=instance.order_sn, 
                total_price=str(instance.pay_price), 
                subject=instance.name, 
                return_url=callback_url, 
                notify_url=url
            )
        except Exception as e:
            alipay_sdk.logger.error(e)
            # assert ValueError('支付异常')
        return url