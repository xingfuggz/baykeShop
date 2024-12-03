#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :serializers.py
@说明    :创建订单序列化器
@时间    :2024/12/03 22:41:22
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from baykeshop.contrib.shop.models import (
    BaykeShopOrders, BaykeShopOrdersGoods, BaykeShopGoodsSKU, 
    BaykeShopCarts, BaykeShopGoodsImages
)
 

class BaykeShopOrdersCreateSerializer(serializers.Serializer):
    """订单创建序列化器"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    source = serializers.ChoiceField(choices=('carts', 'spu'), default='spu', help_text=_('订单来源'))
    quantity = serializers.IntegerField(
        help_text=_('商品数量,只在渠道为spu时需要携带'), 
        default=1, 
        required=False, 
        min_value=1
    )
    skuids = serializers.CharField(help_text=_('商品id,多个以英文逗号隔开'), required=True)
    receiver = serializers.CharField(max_length=50, help_text=_('收货人'), required=True)
    phone = serializers.CharField(max_length=11, help_text=_('手机号码'), required=True)
    address = serializers.CharField(max_length=255, help_text=_('收货地址'), required=True)
    
    def validate(self, attrs):
        request = self.context['request']
        source = attrs.get('source')
        if source == 'spu':
            attrs['skuids'] = [int(attrs.get('skuids'))]
            skus_queryset = BaykeShopGoodsSKU.objects.filter(id__in=attrs['skuids'])
            if not skus_queryset.exists():
                raise serializers.ValidationError(_('商品不存在'))
            # 判断库存
            if skus_queryset.first().stock < int(attrs['quantity']):
                raise serializers.ValidationError(_('库存不足'))
            # 获取商品,传递给create()
            attrs['skus'] = skus_queryset

        elif source == 'carts':
            attrs['skuids'] = [int(skuid) for skuid in attrs.get('skuids').split(',')]
            carts = BaykeShopCarts.objects.filter(user=request.user, sku_id__in=attrs['skuids'])

            if not carts.exists():
                raise serializers.ValidationError('购物车中没有该商品')
            
            for cart in carts:
                # 判断库存
                if cart.sku.stock < cart.quantity:
                    raise serializers.ValidationError('库存不足')
                
            # 获取商品,传递给create()
            attrs['carts'] = carts
        return super().validate(attrs)

    def create(self, validated_data):
        if validated_data.get('source') == 'carts':
            carts = validated_data.get('carts')
            pay_price = sum([cart.total_price for cart in carts])
            orders = self.create_orders(validated_data, pay_price)
            # 批量创建
            BaykeShopOrdersGoods.objects.bulk_create([
                BaykeShopOrdersGoods(
                    site=self.context['request'].site,
                    orders=orders, 
                    sku=cart.sku, 
                    quantity=cart.quantity,
                    price=cart.price,
                    specs=cart.specs,
                    name=cart.name,
                    detail=cart.sku.goods.detail,
                    image=BaykeShopGoodsImages.objects.filter(goods=cart.sku.goods).first().image
                ) for cart in carts
            ])
            # 删除购物车
            carts.delete()
        else:
            sku = validated_data.get('skus').first()
            quantity = validated_data.get('quantity')
            pay_price = sku.price * int(validated_data.get('quantity'))
            orders = self.create_orders(validated_data, pay_price)
            goods = BaykeShopOrdersGoods(
                site=self.context['request'].site,
                orders=orders, 
                sku=sku, 
                quantity=quantity,
                price=sku.price,
                specs=sku.specs,
                name=sku.goods.name,
                detail=sku.goods.detail,
                image=BaykeShopGoodsImages.objects.filter(goods=sku.goods).first().image
            )
            goods.save()
        validated_data['order_sn'] = orders.order_sn
        return validated_data
    
    def create_orders(self, validated_data, pay_price):
        """ 创建订单 """
        orders = BaykeShopOrders(
            site=self.context['request'].site,
            pay_price=pay_price,
            user=validated_data.get('user'),
            receiver=validated_data.get('receiver'),
            phone=validated_data.get('phone'),
            address=validated_data.get('address'),
        )
        orders.save()
        return orders
