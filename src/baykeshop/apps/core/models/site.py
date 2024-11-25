from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from .abstract import BaseModel


class ExtendSite(BaseModel):
    """ 站点扩展 """
    site = models.OneToOneField(Site, on_delete=models.CASCADE, verbose_name=_('站点'), related_name='extend_site')
    site_title = models.CharField(max_length=50, verbose_name=_('标题'), help_text=_('用于SEO优化, 前后台显示的站点名称'))
    site_header = models.CharField(max_length=50, verbose_name=_('头部'), blank=True, default='', help_text=_('管理后台使用的站点名称'))
    index_title = models.CharField(max_length=50, verbose_name=_('首页标题'), blank=True, default='', help_text=_('管理后台首页标题'))
    logo = models.ImageField(upload_to='site/logo/%Y/%m/%d', verbose_name=_('logo'), blank=True, default='', help_text=_('站点Logo'))
    description = models.TextField(verbose_name=_('描述'), blank=True, default='', help_text=_('用于SEO优化, 前台显示的站点描述'))
    keywords = models.TextField(verbose_name=_('关键字'), blank=True, default='', help_text=_('用于SEO优化, 前台显示的站点关键字'))
    icp_record = models.CharField(max_length=50, verbose_name=_('备案号'), blank=True, default='陕ICP备123456789')

    class Meta:
        verbose_name = _('站点扩展')
        verbose_name_plural = _('站点扩展')
        ordering = ('-create_time',)

    def __str__(self):
        return self.site.name


class ExtandSiteConfig(BaseModel):
    """ 站点扩展配置  """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name=_('站点'), related_name='extend_site_config')
    key = models.CharField(max_length=50, verbose_name=_('键'))
    value = models.TextField(verbose_name=_('值'))
    description = models.CharField(verbose_name=_('描述'), blank=True, default='', max_length=50)

    class Meta:
        verbose_name = _('站点扩展配置')
        verbose_name_plural = _('站点扩展配置')
        ordering = ('-create_time',)
        constraints = [
            models.UniqueConstraint(fields=['site', 'key'], name='unique_site_key')
        ]

    def __str__(self):
        return self.description
    
    def natural_key(self):
        return (self.site, self.key)


class ExtendSiteEmail(BaseModel):
    """ 站点邮箱配置 """
    site = models.OneToOneField(Site, on_delete=models.CASCADE, verbose_name=_('站点'), related_name='extend_site_email')
    host = models.CharField(max_length=50, verbose_name=_('主机'))
    port = models.PositiveSmallIntegerField(default=465, verbose_name=_('端口'))
    username = models.CharField(max_length=50, verbose_name=_('用户名'))
    password = models.CharField(max_length=50, verbose_name=_('密码'))
    is_ssl = models.BooleanField(default=False, verbose_name=_('是否SSL'))
    is_tls = models.BooleanField(default=False, verbose_name=_('是否TLS'))
    from_email = models.EmailField(verbose_name=_('发件人'), blank=True, default='')

    class Meta:
        verbose_name = _('站点邮箱配置')
        verbose_name_plural = _('站点邮箱配置')
        ordering = ('-create_time',)
    
    def __str__(self):
        return self.host
    
    def save(self, *args, **kwargs):
        if self.is_ssl and self.is_tls:
            raise ValueError('SSL和TLS不能同时开启')
        super().save(*args, **kwargs)

    def send_email(self, subject, message, to_email):
        from django.core.mail import EmailMultiAlternatives
        msg = EmailMultiAlternatives(subject, message, self.from_email, to_email)
        msg.send()
        return True
    
    def send_email_template(self, template_name, context, to_email):
        from django.template.loader import render_to_string
        from django.core.mail import EmailMultiAlternatives
        subject = render_to_string(template_name + '.subject.txt', context)
        message = render_to_string(template_name + '.html', context)
        msg = EmailMultiAlternatives(subject, message, self.from_email, to_email)
        msg.attach_alternative(message, 'text/html')
        msg.send()
        return True
    

    
