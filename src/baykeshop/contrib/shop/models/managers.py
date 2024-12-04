from django.db import models

from baykeshop.db.base import BaseManager


class BaykeShopGoodsManager(BaseManager):
    """商品管理器"""
    def get_queryset(self):
        from baykeshop.contrib.shop.models import BaykeShopGoodsImages
        return super().get_queryset().alias(
            price=models.Min('baykeshopgoodssku__price'),
            sales=models.Sum('baykeshopgoodssku__sales'),
            stock=models.Min('baykeshopgoodssku__stock'),
            line_price=models.Min('baykeshopgoodssku__line_price'),
        ).annotate(
            price=models.F('price'),
            sales=models.F('sales'),
            stock=models.F('stock'),
            line_price=models.F('line_price'),
            image_url = models.Subquery(
                BaykeShopGoodsImages.objects.filter(
                    goods=models.OuterRef('pk'),
                ).values('image')[:1],
                output_field=models.CharField()
            )
        ).prefetch_related('baykeshopgoodssku_set', 'baykeshopgoodsimages_set')


class BaykeShopCartsManager(BaseManager):
    """购物车管理器"""
    def get_queryset(self):
        from baykeshop.contrib.shop.models import BaykeShopGoodsImages
        return super().get_queryset().select_related('sku').alias(
            total_price=models.ExpressionWrapper(
                models.F('quantity') * models.F('sku__price'),
                output_field=models.DecimalField()
            ),
            name=models.F('sku__goods__name'),
            specs=models.F('sku__specs'),
            price=models.F('sku__price'),
        ).annotate(
            total_price=models.F('total_price'),
            name=models.F('name'),
            specs=models.F('specs'),
            image_url = models.Subquery(
                BaykeShopGoodsImages.objects.filter(
                    goods=models.OuterRef('sku__goods'),
                ).values('image')[:1],
                output_field=models.CharField()
            ),
            price=models.F('price'),
        )
    

class BaykeShopGoodsSKUManager(models.Manager):
    """ sku 管理器 """
    def get_queryset(self):
        from baykeshop.contrib.shop.models import BaykeShopGoodsImages
        queryset = super().get_queryset().select_related('goods').alias(
            name=models.F('goods__name'),
            detail=models.F('goods__detail'),
            goods_type=models.F('goods__goods_type'),
            image_url=models.Subquery(
                BaykeShopGoodsImages.objects.filter(
                    goods=models.OuterRef('goods'),
                ).values('image')[:1],
                output_field=models.CharField()
            )
        ).annotate(
            name = models.F('goods__name'),
            image_url = models.F('image_url'),
            detail=models.F('goods__detail'),
            goods_type=models.F('goods__goods_type'),
        )
        return queryset


class BaykeShopOrdersManager(BaseManager):
    """订单管理器"""
    def get_queryset(self):
        return super().get_queryset().prefetch_related('baykeshopordersgoods_set').alias(
            total_price=models.ExpressionWrapper(
                models.Sum(models.F('baykeshopordersgoods__quantity') * models.F('baykeshopordersgoods__price')),
                output_field=models.DecimalField()
            ),
            total_quantity=models.Sum('baykeshopordersgoods__quantity'),
            name=models.F('baykeshopordersgoods__name')
        ).annotate(
            total_price=models.F('total_price'),
            total_quantity=models.F('total_quantity'),
            name=models.F('name')
        )


class BaykeShopOrdersGoodsManager(BaseManager):
    """订单商品管理器"""
    def get_queryset(self):
        from baykeshop.contrib.shop.models import BaykeShopGoodsImages
        return super().get_queryset().select_related('sku').alias(
            name=models.F('sku__goods__name'),
            specs=models.F('sku__specs'),
            image_url = models.Subquery(
                BaykeShopGoodsImages.objects.filter(
                    goods=models.OuterRef('sku__goods'),
                ).values('image')[:1],
                output_field=models.CharField()
            )
        )