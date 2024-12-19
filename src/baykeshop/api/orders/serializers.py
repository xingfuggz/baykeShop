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

from django.db.models.signals import post_save
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from rest_framework import serializers

from baykeshop.contrib.shop.models import (
    BaykeShopOrdersGoods, BaykeShopOrders, BaykeShopGoodsImages,
    BaykeShopCarts
)

 
class BaykeShopOrdersGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaykeShopOrdersGoods
        fields = ('sku', 'quantity')


class BaykeShopOrdersCreateSerializer(serializers.ModelSerializer):
    """订单创建序列化器"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    baykeshopordersgoods_set = BaykeShopOrdersGoodsSerializer(many=True)
    """ 创建订单的几种方式
        carts: 购物车，这里会查找购物车去清理数据
        default: 直接创建不做任何处理
    """
    source = serializers.ChoiceField(
        choices=('carts', 'default'), 
        help_text=_('订单来源'), 
        required=False,
        write_only=True,
        default='default'
    )
    pay_url = serializers.CharField(required=False, read_only=True, help_text=_('支付地址'))

    class Meta:
        model = BaykeShopOrders
        fields = (
            'user', 'baykeshopordersgoods_set', 
            'receiver', 'phone', 'address', 'source',
            'pay_url'
        )
    
    def validate(self, attrs):
        """验证数据"""
        baykeshopordersgoods_set = attrs.get('baykeshopordersgoods_set')
        if not baykeshopordersgoods_set:
            raise serializers.ValidationError(_('请选择商品'))
        for item in baykeshopordersgoods_set:
            if int(item['quantity']) <= 0:
                raise serializers.ValidationError(_('商品数量必须大于0'))
            sku = item.get('sku')
            if sku.stock < int(item['quantity']):
                raise serializers.ValidationError(_('商品库存不足'))
        return attrs

    def create(self, validated_data):
        """创建订单"""
        source = validated_data.pop('source')
        baykeshopordersgoods_set = validated_data.pop('baykeshopordersgoods_set')
        pay_price = sum([item['sku'].price * item['quantity'] for item in baykeshopordersgoods_set])
        orders = BaykeShopOrders.objects.create(pay_price=pay_price, **validated_data)
        created_objects = BaykeShopOrdersGoods.objects.bulk_create(
            [BaykeShopOrdersGoods(orders=orders, **self.goods_format(item)) for item in baykeshopordersgoods_set]
        )
        # 手动触发post_save信号
        for obj in created_objects:
            post_save.send(sender=BaykeShopOrdersGoods, instance=obj, created=True)
        # 清理购物车数据
        if source == 'carts':
            skus = [item['sku'] for item in baykeshopordersgoods_set]
            BaykeShopCarts.objects.filter(user=validated_data['user'], sku__in=skus).delete()
        orders.pay_url = reverse('shop:orders-pay', kwargs={'order_sn': orders.order_sn})
        messages.success(self.context['request'], _('订单创建成功, 请尽快支付, 否则订单会自动取消'))
        return orders
    
    def get_image(self, sku):
        images = BaykeShopGoodsImages.objects.filter(goods=sku.goods)
        if images.exists():
            return images.first().image
        return ''

    def goods_format(self, item):
        """商品格式化"""
        item['price'] = item['sku'].price
        item['sku_sn'] = item['sku'].sku_sn
        item['name'] = item['sku'].goods.name
        item['image'] = self.get_image(item['sku'])
        item['specs'] = item['sku'].specs
        item['detail'] = item['sku'].goods.detail
        return item