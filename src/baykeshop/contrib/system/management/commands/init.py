from django.core import management
from django.core.management.base import BaseCommand
from baykeshop.conf import bayke_settings


class Command(BaseCommand):
    help = "初始化项目数据"

    def handle(self, *args, **options):
        site_id = bayke_settings.SITE_ID
        management.call_command(
            "add_dict", 
            site_id, 'SITE_TITLE', "站点名称", 
            bayke_settings.SITE_TITLE
        )
        management.call_command(
            "add_dict", 
            site_id, 'SITE_HEADER', "管理后台使用的站点名称", 
            bayke_settings.SITE_HEADER
        )
        management.call_command(
            "add_dict", 
            site_id, 'INDEX_TITLE', "管理后台首页标题", 
            bayke_settings.INDEX_TITLE
        )
        management.call_command(
            "add_dict", 
            site_id, 'SITE_DESCRIPTION', "站点描述", 
            bayke_settings.DESCRIPTION
        )
        management.call_command(
            "add_dict", 
            site_id, 'SITE_KEYWORDS', "站点关键字", 
            bayke_settings.KEYWORDS
        )
        management.call_command(
            "add_dict", 
            site_id, 'COPYRIGHT', "版权信息", 
            bayke_settings.COPYRIGHT
        )
        management.call_command(
            "add_dict", 
            site_id, 'EMAIL_HOST', "SMTP 服务器地址", 
            bayke_settings.EMAIL_HOST
        )
        management.call_command(
            "add_dict", 
            site_id, 'EMAIL_PORT', "SMTP 服务器端口", 
            bayke_settings.EMAIL_PORT
        )
        management.call_command(
            "add_dict", 
            site_id, 'EMAIL_HOST_USER', "SMTP 服务器用户名", 
            bayke_settings.EMAIL_HOST_USER
        )
        management.call_command(
            "add_dict", 
            site_id, 'EMAIL_HOST_PASSWORD', "SMTP 服务器密码", 
            bayke_settings.EMAIL_HOST_PASSWORD
        )
        management.call_command(
            "add_dict", 
            site_id, 'EMAIL_USE_TLS', "SMTP 服务器是否使用 TLS", 
            bayke_settings.EMAIL_USE_TLS
        )
        management.call_command(
            "add_dict", 
            site_id, 'EMAIL_USE_SSL', "SMTP 服务器是否使用 SSL", 
            bayke_settings.EMAIL_USE_SSL
        )
        management.call_command(
            "add_dict", 
            site_id, 'ALIPAY_APPID', "支付宝 APPID", 
            bayke_settings.ALIPAY_APPID
        )
        management.call_command(
            "add_dict", 
            site_id, 'ALIPAY_PUBLIC_KEY', "支付宝公钥", 
            bayke_settings.ALIPAY_PUBLIC_KEY
        )
        management.call_command(
            "add_dict", 
            site_id, 'ALIPAY_PRIVATE_KEY', "支付宝私钥", 
            bayke_settings.ALIPAY_PRIVATE_KEY
        )
        management.call_command(
            "add_dict", 
            site_id, 'ICP', "备案号", 
            bayke_settings.ICP
        )
        management.call_command("createmenus")
