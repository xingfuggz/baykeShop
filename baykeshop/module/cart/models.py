#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :cart.py
@说明    :购物车模型
@时间    :2023/02/08 21:02:24
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.contrib.auth import get_user_model

from baykeshop.models import _abs
from baykeshop.models import product

User = get_user_model()


class BaykeShopingCart(_abs.BaseModelMixin):
    """ 购物车数据模型 """
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_abs._("用户"))
    sku = models.ForeignKey(product.BaykeProduct, on_delete=models.PROTECT, verbose_name=_abs._("商品"))
    num = models.PositiveIntegerField(default=0, verbose_name=_abs._("数量"))
    
    class Meta:
        verbose_name = _abs._('购物车')
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['owner', 'sku'], name='unique_owner_sku')
        ]
        
    def __str__(self):
        return f'{self.owner}{self.sku}'
    
    @classmethod
    def get_cart_count(cls, user):
        # 当前用户的购物车商品数量
        return sum(list(cls.objects.filter(owner=user).values_list('num', flat=True)))