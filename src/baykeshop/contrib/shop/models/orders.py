from django.db import models
from django.utils.translation import gettext_lazy as _

from baykeshop.db import BaseOrdersModel, BaseOrdersGoodsModel
from .goods import BaykeShopGoodsSKU


class BaykeShopOrders(BaseOrdersModel):
    """订单表"""

    class Meta(BaseOrdersModel.Meta):
        verbose_name = _('订单')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        
    def __str__(self):
        return self.order_sn
    

class BaykeShopOrdersGoods(BaseOrdersGoodsModel):
    """订单商品表"""
    sku = models.ForeignKey(BaykeShopGoodsSKU, on_delete=models.CASCADE, verbose_name=_('商品'))
    orders = models.ForeignKey(BaykeShopOrders, on_delete=models.CASCADE, verbose_name=_('订单'))

    class Meta:
        verbose_name = _('订单商品')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        constraints = [
            models.UniqueConstraint(fields=['sku', 'orders'], name='sku_orders_unique')
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """ 创建时自动获取sku信息 """
        self.name = self.sku.goods.name
        self.price = self.sku.price
        self.detail = self.sku.goods.detail
        self.image = self.sku.goods.image
        self.sku_sn = self.sku.sku_sn
        self.specs = self.sku.specs
        super().save(*args, **kwargs)