from django.conf import settings
from django.urls import NoReverseMatch, reverse


from baykeshop.conf import bayke_settings
from baykeshop.module.payment.alipay import AliPay, AliPayConfig


class AlipayMethod:
    
    appid = "2021000116697536"
    public_key_string_path = bayke_settings.ALIPAY_PUBLIC_KEY
    private_key_string_path = bayke_settings.ALIPAY_PRIVATE_KEY
    
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
    
    @property
    def notify_url(self):
        url = reverse("baykeshop:home")
        try:
            url = reverse(bayke_settings.ALIPAY_NOTIFY_URL)
        except NoReverseMatch:
            pass
        # url = f"{self.request.scheme}://{self.request.get_host()}{url}"
        return url
    
    def alipay(self):
        return AliPay(
            appid=self.appid,
            app_notify_url=self.notify_url,
            app_private_key_string=self.private_key_string,
            alipay_public_key_string=self.public_key_string,
            sign_type="RSA2",
            debug=settings.DEBUG,
            verbose=False,
            config=AliPayConfig()
        )
    
    def biz_content(self):
        alipay = self.alipay()
        url_params = alipay.api_alipay_trade_page_pay(
                    subject='123456789',
                    total_amount=15,
                    out_trade_no='123456789',
                    return_url=self.notify_url,
                    notify_url=self.notify_url
                )
        return url_params
    
pay = AlipayMethod()



# from baykeshop.module.payment.alipay import AliPay, AliPayConfig
# from baykeshop.config.settings import bayke_settings

# private_key_string
# with open(bayke_settings.ALIPAY_PRIVATE_KEY, 'r') as f:
#     private_key_string = f.read()

# # public_key_string
# with open(bayke_settings.ALIPAY_PUBLIC_KEY, 'r') as f:
#     public_key_string = f.read()


alipay = AliPay(
    appid=bayke_settings.ALIPAY_APPID,
    app_notify_url=None,  # 默认回调 url
    app_private_key_string=pay.private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=pay.public_key_string,
    sign_type=bayke_settings.ALIPAY_SIGN_TYPE,  # RSA 或者 RSA2
    debug=bayke_settings.ALIPAY_DEBUG,  # 默认 False
    verbose=bayke_settings.ALIPAY_DEBUG,  # 输出调试数据
    config=AliPayConfig(timeout=bayke_settings.ALIPAY_TIMOUT)  # 可选，请求超时时间
)