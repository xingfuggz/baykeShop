#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :urls.py
@说明    :接口路由总文件
@时间    :2024/12/01 09:51:50
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from django.urls import path
from rest_framework import routers

from baykeshop.api.carts import views as carts_views
from baykeshop.api.orders import views as orders_views


router = routers.DefaultRouter()
# 路由命名空间
app_name = 'baykeshop_api'
# 购物车
router.register('carts', carts_views.BaykeShopCartsViewSet, basename='carts')

urlpatterns = [
    path(
        'orders/', 
        orders_views.BaykeShopOrdersGenericAPIView.as_view(), 
        name='orders-create'
    ),
    *router.urls
]