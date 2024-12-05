from django.db import models
from django.utils.translation import gettext_lazy as _
from baykeshop.db import BaseModel


class BaykeBanners(BaseModel):
    """
    轮播图
    """
    title = models.CharField(max_length=50, verbose_name=_('标题'))
    image = models.ImageField(upload_to='banners', verbose_name=_('图片'))
    url = models.CharField(max_length=255, blank=True, default='', verbose_name=_('链接'))
    order = models.IntegerField(default=0, verbose_name=_('排序'))
    is_show = models.BooleanField(default=True, verbose_name=_('是否显示'))

    class Meta:
        verbose_name = _('轮播图')
        verbose_name_plural = _('轮播图')
        ordering = ('-order',)
    
    def __str__(self):
        return self.title