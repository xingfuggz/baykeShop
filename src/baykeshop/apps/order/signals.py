from django.db.models.signals import post_save
from django.dispatch import receiver

from baykeshop.apps.order.models import BaykeShopOrderItem


@receiver(post_save, sender=BaykeShopOrderItem)
def sku_stock_sales_update(sender, instance, **kwargs):
    """ 订单关联商品保存成功 减库存 加销量 """
    from django.db.models import F
    sku = instance.sku
    sku.stock = F("stock") - instance.quantity
    sku.num = F("num") + instance.quantity
    sku.save()