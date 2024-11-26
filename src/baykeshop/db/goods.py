from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .base import BaseModel

User = get_user_model()


class BaseGoodsModel(BaseModel):
    """商品表"""
    name = models.CharField(max_length=50, verbose_name=_('商品名称'))
    keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('商品关键字'))
    description = models.TextField(blank=True, null=True, verbose_name=_('商品描述'))
    detail = models.TextField(blank=True, null=True, verbose_name=_('商品详情'))
    image = models.ImageField(upload_to='goods', blank=True, null=True, verbose_name=_('商品主图'))
    images = models.JSONField(blank=True, null=True, verbose_name=_('商品轮播图'), default=list)
    is_multi = models.BooleanField(default=False, verbose_name=_('是否多规格'))

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品')
        ordering = ['-created_time']
        abstract = True
    

class BaseGoodsSKUModel(BaseModel):
    """ 商品规格 """
    specs = models.JSONField(
        verbose_name=_('规格'), 
        default=list,
        help_text=_('规格数据'),
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('价格'))
    sku_sn = models.CharField(max_length=50, verbose_name=_('商品编码'), blank=True, default='')
    # 划线价
    line_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_('划线价'), 
        blank=True, 
        default='',
        help_text=_('商品价格划线价，不参与价位计算筛选, 仅供前端显示使用')
    )
    stock = models.PositiveSmallIntegerField(default=0, verbose_name=_('库存'))
    sales = models.PositiveSmallIntegerField(default=0, verbose_name=_('销量'))

    class Meta:
        verbose_name = _('商品规格')
        verbose_name_plural = _('商品规格')
        ordering = ['-created_time']
        abstract = True


