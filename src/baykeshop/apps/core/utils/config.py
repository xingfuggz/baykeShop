from django.contrib.sites.models import Site
from baykeshop.apps.core.models import ExtandSiteConfig, ExtendSiteEmail, ExtendSite
from baykeshop.config import bayke_settings


class DoesNotExistSite(Exception): pass
class DoesNotExistSiteConfig(Exception): pass
class DoesNotExistSiteEmail(Exception): pass


class SiteConfig:
    """ 站点配置类 """
    SITE_ID = bayke_settings.SITE_ID
    def __init__(self, site=None):
        self.site = site

    def get_site(self):
        """ 获取站点 """
        if self.site is None:
            try:
                self.site = Site.objects.get(id=self.SITE_ID)
            except Site.DoesNotExist:
                raise DoesNotExistSite('站点不存在, 请先添加站点')
        return self.site

    def get_site_config(self, key):
        """ 获取配置 """
        site = self.get_site()
        try:
            return ExtandSiteConfig.objects.get(site=site, key=key)
        except ExtandSiteConfig.DoesNotExist:
            raise DoesNotExistSiteConfig(f'配置{key}不存在, 清先添加配置')
    
    def get_site_email(self):
        """ 获取站点邮件配置 """
        site = self.get_site()
        try:
            return ExtendSiteEmail.objects.get(site=site)
        except ExtendSiteEmail.DoesNotExist:
            raise DoesNotExistSiteEmail('邮件配置不存在, 清先初始化站点配置')
        
    def get_site_extend(self):
        """ 获取站点扩展 """
        site = self.get_site()
        try:
            return ExtendSite.objects.get(site=site)
        except ExtendSite.DoesNotExist:
            raise DoesNotExistSite('站点扩展不存在, 清先初始化站点扩展')    
    
    def get_site_config_value(self, key):
        """ 获取配置值 """
        return self.get_site_config(key).value
    
    def get_site_email_value(self, key:str):
        """ 获取邮件配置值 """
        return self.get_site_email().__getattribute__(key)
    
    def get_site_extend_value(self, key:str):
        """ 获取扩展值 """
        return self.get_site_extend().__getattribute__(key)
    
    def create_site_config(self, key, value, description:str):
        """ 创建配置 """
        site = self.get_site()
        config, iscreated = ExtandSiteConfig.objects.update_or_create(
            site=site, key=key, 
            defaults={
                'key': key,
                'value': value, 
                'description': description
                }
            )
        return config
    
    def create_site_email(self, **kwargs):
        """ 创建邮件配置 """
        site = self.get_site()
        obj, iscreated = ExtendSiteEmail.objects.update_or_create(site=site, defaults=kwargs)
        return obj
    
    def create_site_extend(self, **kwargs):
        """ 创建扩展 """
        site = self.get_site()
        obj, iscreated = ExtendSite.objects.update_or_create(site=site, defaults=kwargs)
        return obj
