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
from baykeshop.api.pay import views as pay_views
from baykeshop.api.comments import views as comments_views
from baykeshop.api.upload import views as upload_views


router = routers.DefaultRouter()
# 路由命名空间
app_name = 'baykeshop_api'
# 购物车
router.register('carts', carts_views.BaykeShopCartsViewSet, basename='carts')

"""
支付订单,处理支付逻辑
根据选择的支付方式返回对应的支付地址
    @url: {% url 'baykeshop_api:pay-detail' order_sn=订单编号 %}
    @method: post
"""
router.register('pay', pay_views.BaykeShopOrdersPayView, basename='pay')
# 订单评论
router.register('comments', comments_views.BaykeShopOrdersCommentViewSet, basename='comments')

"""
创建订单及删除订单
1.创建订单 
    @url: {% url 'baykeshop_api:orders-list' %} 
    @method: post
2.删除订单 
    @url: {% url 'baykeshop_api:orders-detail' order_sn=订单编号 %} 
    @method: delete
"""
router.register('orders', orders_views.BaykeShopOrdersViewSet, basename='orders')

urlpatterns = [
    path('upload/image/', upload_views.UploadImageView.as_view(), name='upload-image'),
    *router.urls
]