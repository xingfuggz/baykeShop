from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from baykeshop.db import BaseModel


class BaykeGalleryCategory(BaseModel):
    """图库分类"""
    name = models.CharField(max_length=50, verbose_name=_('分类名称'))
    
    class Meta:
        verbose_name = _('图库分类')
        verbose_name_plural = _('图库分类')
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class BaykeGallery(BaseModel):
    """图库"""
    category = models.ForeignKey(BaykeGalleryCategory, on_delete=models.CASCADE, verbose_name=_('图库分类'))
    image = models.ImageField(upload_to='gallery', verbose_name=_('图片'))

    class Meta:
        verbose_name = _('图库')
        verbose_name_plural = _('图库')
        ordering = ['-created_time']
    
    def __str__(self):
        return self.category.name
