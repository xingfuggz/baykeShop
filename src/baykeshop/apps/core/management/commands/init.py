from django.core import management
from django.core.management.base import BaseCommand

from baykeshop.apps.core.utils.config import SiteConfig
from baykeshop.config import bayke_settings

site_config = SiteConfig()

class Command(BaseCommand):
    help = "初始化项目数据"

    def handle(self, *args, **options):
        # 站点
        site_config.create_site_extend(
            site_title=bayke_settings.SITE_TITLE, 
            site_header=bayke_settings.SITE_HEADER, 
            index_title=bayke_settings.INDEX_TITLE, 
            description=bayke_settings.DESCRIPTION, 
            keywords=bayke_settings.KEYWORDS, 
        )
        # 邮箱
        site_config.create_site_email(
            host=bayke_settings.EMAIL_HOST, 
            port=bayke_settings.EMAIL_PORT, 
            username=bayke_settings.EMAIL_HOST_USER, 
            password=bayke_settings.EMAIL_HOST_PASSWORD, 
            is_ssl=bayke_settings.EMAIL_USE_SSL, 
            is_tls=bayke_settings.EMAIL_USE_TLS, 
        )
        # 支付宝支付初始配置
        site_config.create_site_config(
            key='ALIPAY_APPID', 
            value=bayke_settings.ALIPAY_APPID,
            description='支付宝APPID'
        )
        site_config.create_site_config(
            key='ALIPAY_PRIVATE_KEY', 
            value=bayke_settings.ALIPAY_PRIVATE_KEY,
            description='支付宝私钥'
        )
        site_config.create_site_config(
            key='ALIPAY_PUBLIC_KEY', 
            value=bayke_settings.ALIPAY_PUBLIC_KEY,
            description='支付宝公钥'
        )
        site_config.create_site_config(
            key='COPYRIGHT', 
            value=bayke_settings.COPYRIGHT,
            description='底部版权信息'
        )

        self.stdout.write(self.style.SUCCESS('项目数据初始化完成'))