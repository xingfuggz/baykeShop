#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :serializers.py
@说明    :购物车模块序列化类
@时间    :2024/12/01 09:26:32
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from baykeshop.contrib.shop.models import BaykeShopCarts


User = get_user_model()


class BaykeShopCartsSerializer(serializers.ModelSerializer):
    """ 加入购物车序列化类 """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BaykeShopCarts
        fields = ('user', 'sku', 'quantity')
        validators = []

    def create(self, validated_data):
        # 判断是否已经在购物车，如果在，则仅更新数量
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            queryset = BaykeShopCarts.objects.filter(
                user=validated_data['user'],
                sku=validated_data['sku']
            )
            queryset.update(quantity=models.F('quantity') + validated_data['quantity'])
            instance = queryset.first()
        return instance
    
    def update(self, instance, validated_data):
        instance.quantity = validated_data['quantity']
        instance.save()
        messages.success(self.context['request'], _('更新购物车数量成功'))
        return instance
