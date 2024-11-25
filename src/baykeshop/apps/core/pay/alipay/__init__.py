import logging
import traceback

from django.conf import settings
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)

logger = logging.getLogger('')

"""
设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
"""
alipay_client_config = AlipayClientConfig()
alipay_client_config.server_url = (
    'https://openapi-sandbox.dl.alipaydev.com/gateway.do' 
    if settings.DEBUG else 
    'https://openapi.alipay.com/gateway.do'
)
alipay_client_config.app_id = ''
alipay_client_config.app_private_key = ''
alipay_client_config.alipay_public_key = ''
"""
得到客户端对象。
注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
logger参数用于打印日志，不传则不打印，建议传递。
"""
client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
"""
构建请求参数，使用kwargs方式传入，支持传入任意参数，具体参数含义请查看文档。
"""
request = AlipayTradePagePayRequest(biz_model=AlipayTradePagePayModel())

def pay(order_sn, total_price, subject, return_url, notify_url):
    """
    支付
    """
    request.biz_model.out_trade_no = order_sn
    request.biz_model.total_amount = total_price
    request.biz_model.subject = subject
    request.biz_model.product_code = "FAST_INSTANT_TRADE_PAY"
    request.return_url = return_url
    request.notify_url = notify_url
    response = client.page_execute(request, http_method="GET")
    return response

def get_alipay_public_key():
    """
    获取支付宝公钥
    """
    return alipay_client_config.alipay_public_key

def get_sign_type():
    """
    获取签名类型
    """
    return alipay_client_config.sign_type

def get_alipay_gateway_url():
    """
    获取支付宝网关地址
    """
    return alipay_client_config.server_url

def get_app_id():
    """
    获取app_id
    """
    return alipay_client_config.app_id

def get_app_private_key():
    """
    获取应用私钥
    """
    return alipay_client_config.app_private_key