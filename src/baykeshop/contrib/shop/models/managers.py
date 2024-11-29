from django.db import models

from baykeshop.db.base import BaseManager


class BaykeShopGoodsManager(BaseManager):
    """商品管理器"""
    def get_queryset(self):
        return super().get_queryset().alias(
            price=models.Min('baykeshopgoodssku__price'),
            sales=models.Sum('baykeshopgoodssku__sales'),
            stock=models.Min('baykeshopgoodssku__stock'),
            line_price=models.Min('baykeshopgoodssku__line_price')
        ).annotate(
            price=models.F('price'),
            sales=models.F('sales'),
            stock=models.F('stock'),
            line_price=models.F('line_price')
        ).prefetch_related('baykeshopgoodssku_set')
    

class BaykeShopCartsManager(BaseManager):
    """购物车管理器"""
    def get_queryset(self):
        return super().get_queryset().select_related('sku').alias(
            total_price=models.ExpressionWrapper(
                models.F('quantity') * models.F('sku__price'),
                output_field=models.DecimalField()
            ),
            image=models.F('sku__goods__image'),
            name=models.F('sku__goods__name'),
            specs=models.F('sku__specs')
        )
    

class BaykeShopOrdersManager(BaseManager):
    """订单管理器"""
    def get_queryset(self):
        return super().get_queryset().alias(
            total_price=models.ExpressionWrapper(
                models.Sum(models.F('baykeshopordersgoods__quantity') * models.F('baykeshopordersgoods__price')),
                output_field=models.DecimalField()
            ),
            total_quantity=models.Sum('baykeshopordersgoods__quantity')
        ).annotate(
            total_price=models.F('total_price'),
            total_quantity=models.F('total_quantity')
        )
    
