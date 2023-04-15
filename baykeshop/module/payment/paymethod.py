from django.conf import settings
from django.urls import NoReverseMatch, Resolver404, resolve, reverse

from rest_framework.request import HttpRequest

from baykeshop.module.order.models import BaykeOrderInfo
from baykeshop.module.payment.alipay import AliPay, AliPayConfig
from baykeshop.conf import bayke_settings


class BasePayMethod:
    """ 支付基类 """
    @property
    def redirct_url(self):
        pass
    
    @property
    def notify_url(self):
        pass
    
    @property
    def return_url(self):
        pass

    def notify_view(self):
        pass
    

class AlipayMethod(BasePayMethod):
    """ 支付宝支付 """
    appid = "2021000116697536"
    public_key_string_path = bayke_settings.ALIPAY_PUBLIC_KEY
    private_key_string_path = bayke_settings.ALIPAY_PRIVATE_KEY
    
    def __init__(self, request, orderinfo) -> None:
        self.request = request
        self.orderinfo = orderinfo
        
    @property
    def private_key_string(self):
        """"
        app_private_key_string【应用私钥】格式为：
        -----BEGIN PRIVATE KEY-----
        这里为秘钥信息，上下必须用这个包裹
        -----END PRIVATE KEY-----
        """
        with open(settings.BASE_DIR / self.private_key_string_path, 'r') as f:
            private_key_string = f.read()
        return private_key_string
    
    @property
    def public_key_string(self):
        """
        alipay_public_key_string【支付宝公钥】格式为：
        -----BEGIN PUBLIC KEY-----
        这里为秘钥信息，上下必须用这个包裹
        -----END PUBLIC KEY-----
        """
        with open(settings.BASE_DIR / self.public_key_string_path, 'r') as f:
            public_key_string = f.read()
        return public_key_string
    
    def alipay(self):
        return AliPay(
            appid=self.appid,
            app_notify_url=self.notify_url,
            app_private_key_string=self.private_key_string,
            alipay_public_key_string=self.public_key_string,
            sign_type="RSA2",
            debug=settings.DEBUG,
            verbose=settings.DEBUG,
            config=AliPayConfig()
        )
        
    @property
    def redirct_url_params(self):
        alipay = self.alipay()
        return alipay.api_alipay_trade_page_pay(
            subject=self.orderinfo.order_sn,
            total_amount=self.orderinfo.total_amount.to_eng_string(),
            out_trade_no=self.orderinfo.order_sn,
            return_url=self.return_url,
            notify_url=self.notify_url
        )
        
    @property
    def redirct_url(self):
        redirct_url = self.alipay()._gateway
        return f"{redirct_url}?{self.redirct_url_params}"
   
    @property
    def notify_url(self):
        url = reverse("baykeshop:home")
        try:
            url = reverse(bayke_settings.ALIPAY_NOTIFY_URL)
        except NoReverseMatch:
            pass
        url = f"{self.request.scheme}://{self.request.get_host()}{url}"
        return url
    
    @property
    def return_url(self):
        url = reverse("baykeshop:home")
        try:
            url = reverse(bayke_settings.ALIPAY_RETURN_URL)
        except NoReverseMatch:
            pass
        url = f"{self.request.scheme}://{self.request.get_host()}{url}"
        return url
    

class Pay:
    
    def __call__(self, request:HttpRequest, method:int, orderinfo:BaykeOrderInfo):
        if method == 1:
            return None
        elif method == 2:
            return AlipayMethod(request, orderinfo).redirct_url
        elif method == 3:
            return None
        elif method == 4:
            return None
        else:
            return None

    def __str__(self) -> str:
        return "<Pay: baykeshop.module.payment.paymethod>"