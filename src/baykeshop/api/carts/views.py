#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :购物车模块视图类
@时间    :2024/12/01 09:29:59
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from baykeshop.contrib.shop.models import BaykeShopCarts
from .serializers import BaykeShopCartsSerializer


class BaykeShopCartsViewSet(mixins.ListModelMixin, 
                            mixins.CreateModelMixin, 
                            mixins.DestroyModelMixin, 
                            viewsets.GenericViewSet):
    """购物车模块视图类"""
    pagination_class = PageNumberPagination
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthenticated]
    serializer_class = BaykeShopCartsSerializer

    def get_queryset(self):
        return BaykeShopCarts.objects.filter(user=self.request.user)