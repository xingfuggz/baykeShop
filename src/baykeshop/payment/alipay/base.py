#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件    :base.py
@说明    :封装支付宝支付基础类
@时间    :2024/12/10 15:35:39
@作者    :幸福关中&轻编程
@版本    :1.3.15
@微信    :baywanyun
"""

import logging
import traceback

from django.conf import settings
from django.contrib import messages

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

from baykeshop.contrib.system.models import BaykeDictModel
from baykeshop.contrib.shop.models import BaykeShopOrders


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    filemode="a",
)

logger = logging.getLogger("")


class Alipay:

    def __init__(
        self,
        appid=None,
        app_private_key=None,
        alipay_public_key=None,
        return_url=None,
        notify_url=None,
        debug=None,
        **kwargs,
    ):
        self.app_id = appid
        self.app_private_key = app_private_key
        self.alipay_public_key = alipay_public_key
        self.return_url = return_url
        self.notify_url = notify_url
        self.debug = debug or settings.DEBUG
        self.extra_params = kwargs

    @property
    def server_url(self):
        if self.debug:
            return "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
        return "https://openapi.alipay.com/gateway.do"

    def config(self, **kwargs):
        _config = AlipayClientConfig()
        _config.app_id = self.app_id or BaykeDictModel.get_key_value("ALIPAY_APPID")
        _config.app_private_key = self.app_private_key or BaykeDictModel.get_key_value(
            "ALIPAY_PRIVATE_KEY"
        )
        _config.alipay_public_key = (
            self.alipay_public_key or BaykeDictModel.get_key_value("ALIPAY_PUBLIC_KEY")
        )
        _config.server_url = self.server_url
        # 参数覆盖
        extra_params = {**self.extra_params, **kwargs}
        _config.sign_type = extra_params.get("sign_type", "RSA2")
        _config.charset = extra_params.get("charset", "utf-8")
        # 其他参数
        for key, value in extra_params.items():
            setattr(_config, key, value)
        return _config

    def client(self, **kwargs):
        """构造一个支付宝请求客户端"""
        _logger = self.extra_params.get("logger") or logger
        return DefaultAlipayClient(
            alipay_client_config=self.config(**kwargs), logger=_logger
        )


class TradePagePay(Alipay):
    """网页支付"""

    def __init__(self, request, instance: BaykeShopOrders = None, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.request = request

    def pay_model(self, **kwargs):
        """支付参数
        :param kwargs: 自定义支付参数，kwargs优先级高于instance
        :return: AlipayTradePagePayModel实例对象
        """
        if self.instance is None and not kwargs:
            # traceback.print_exc()
            logger.error(f"订单对象或参数必须传入其中一个")
            messages.error(self.request, f"订单对象或参数必须传入其中一个")
            raise ValueError(f"订单对象或参数必须传入其中一个")

        model = AlipayTradePagePayModel()
        model.product_code = "FAST_INSTANT_TRADE_PAY"

        if kwargs:
            try:
                model.out_trade_no = kwargs["out_trade_no"]
                model.total_amount = kwargs["total_amount"]
                model.subject = kwargs["subject"]
                return model
            except KeyError:
                # traceback.print_exc()
                logger.error(f"参数必须包含out_trade_no, total_amount, subject")
                messages.error(self.request, f"参数必须包含out_trade_no, total_amount, subject")
                raise ValueError(f"参数必须包含out_trade_no, total_amount, subject")

        model.out_trade_no = self.instance.order_sn
        model.total_amount = str(self.instance.pay_price)
        model.subject = self.instance.order_sn
        return model

    def pay_request(self, **kwargs):
        """支付请求
        :param kwargs: 支付参数
        :return: AlipayTradePagePayRequest实例对象
        """
        request = AlipayTradePagePayRequest(biz_model=self.pay_model(**kwargs))
        request.return_url = self.return_url
        request.notify_url = self.notify_url
        return request

    def pay(self, **kwargs):
        """支付
        :param kwargs:
            支付参数,当实例未传入instance时必须传入该参数{out_trade_no, total_amount, subject}
        :return: 支付URL
        """
        client = self.client()
        request = self.pay_request(**kwargs)
        response = client.page_execute(request, http_method="GET")
        return response
