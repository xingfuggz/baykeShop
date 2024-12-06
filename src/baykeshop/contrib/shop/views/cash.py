#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :cash.py
@说明    :收银台视图
@时间    :2024/12/03 10:49:25
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from baykeshop.contrib.shop.models import BaykeShopGoodsSKU, BaykeShopCarts


class BaykeShopCashView(LoginRequiredMixin, TemplateView):
    """收银台视图"""
    template_name = 'baykeshop/shop/cash.html'
    login_url = 'member:login'
    extra_context = {
        'title': '收银台',
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_carts'] = self.has_carts()
        context['skus'] = self.get_queryset()
        context['total'] = self.get_total_price()
        context['count'] = self.get_total_count()
        return context
    
    def has_carts(self):
        """判断购物车是购物车商品"""
        return 'skuids' in self.kwargs
    
    def get_queryset(self):
        """获取商品数据"""
        skuids = []
        if self.has_carts():
            skuids = [int(skuid) for skuid in self.kwargs.get('skuids').split(',')]
            queryset = BaykeShopCarts.objects.filter(sku_id__in=skuids, user=self.request.user)
            return queryset
        else:
            skuids = [int(self.kwargs.get('skuid'))]
            num = self.kwargs.get('num', 1)
            queryset = BaykeShopGoodsSKU.objects.filter(id__in=skuids).annotate(
                total_price = models.ExpressionWrapper(
                    models.F('price') * models.Value(num, output_field=models.IntegerField()),
                    output_field=models.DecimalField()
                ),
                quantity = models.Value(num, output_field=models.IntegerField()),
            )
            return queryset
    
    def get_total_price(self):
        total = sum([obj.total_price for obj in self.get_queryset()])
        return total
    
    def get_total_count(self):
        total = sum([obj.quantity for obj in self.get_queryset()])
        return total
    
    def get_login_url(self):
        messages.warning(self.request, _('请先登录后操作！'))
        return super().get_login_url()