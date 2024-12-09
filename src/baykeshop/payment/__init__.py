#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :__init__.py
@说明    :封装支付宝支付
@时间    :2024/12/09 22:09:51
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

from baykeshop.contrib.system.models import BaykeDictModel
from baykeshop.contrib.shop.models import BaykeShopOrders


class AliPay:

    def __init__(
        self,
        appid=None,
        app_private_key=None,
        alipay_public_key=None,
        return_url=None,
        notify_url=None,
        debug=False,
        **kwargs,
    ):
        self.app_id = appid or BaykeDictModel.get_key_value("ALIPAY_APPID")
        self.app_private_key = app_private_key or BaykeDictModel.get_key_value(
            "ALIPAY_PRIVATE_KEY"
        )
        self.alipay_public_key = alipay_public_key or BaykeDictModel.get_key_value(
            "ALIPAY_PUBLIC_KEY"
        )
        self.return_url = return_url
        self.notify_url = notify_url
        self.debug = debug
        self.extra_params = kwargs

    @property
    def server_url(self):
        if self.debug:
            return "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
        return "https://openapi.alipay.com/gateway.do"

    @property
    def alipay_config(self):
        """支付宝配置"""
        config = AlipayClientConfig(sandbox_debug=self.debug)
        config.app_id = self.app_id
        config.app_private_key = self.app_private_key
        config.alipay_public_key = self.alipay_public_key
        config.server_url = self.server_url
        config.sign_type = self.extra_params.get("sign_type", "RSA2")
        return config

    def alipay_client(self):
        """支付宝客户端"""
        logger = self.extra_params.get("logger")
        return DefaultAlipayClient(
            alipay_client_config=self.alipay_config, logger=logger
        )

    def trade_page_pay_model(self, instance:BaykeShopOrders):
        """ 支付宝网页支付商品信息
        :param instance: 订单实例
        :return: AlipayTradePagePayModel
        """
        model = AlipayTradePagePayModel()
        model.out_trade_no = instance.order_sn
        model.total_amount = str(instance.pay_price)
        model.subject = instance.order_sn
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        return model
    
    
    def trade_page_pay_request(self, instance):
        """ 支付宝支付请求
        :param instance: BaykeShopOrders
        :return: AlipayTradePagePayRequest
        """
        request = AlipayTradePagePayRequest()
        request.biz_model = self.trade_page_pay_model(instance)
        # callback_url=self.context['request'].build_absolute_uri(reverse('shop:alipay-callback'))
        request.return_url = self.return_url
        request.notify_url = self.notify_url
        return request
    
    def trade_page_pay(self, instance):
        """ 创建支付宝支付请求
        :param instance:BaykeShopOrders
        :return: 支付宝支付链接
        """
        client = self.alipay_client()
        request = self.trade_page_pay_request(instance)
        res = client.page_execute(request, http_method="GET")
        return res
