#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :cart.py
@说明    :购物车视图
@时间    :2024/11/12 13:11:20
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from baykeshop.apps.shop.models import BaykeShopCart
from baykeshop.apps.shop.forms import BaykeShopCartAddForm


class BaykeShopCartListView(LoginRequiredMixin, ListView):
    '''购物车列表'''
    template_name = 'shop/shopcart.html'
    login_url = reverse_lazy('user:login')
    paginate_by = 10

    def get_queryset(self):
        return BaykeShopCart.get_cart_queryset(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_total_price'] = BaykeShopCart.get_cart_total_price(self.request.user)
        print(context['cart_total_price'])
        return context
    

class BaykeShopCartAddView(LoginRequiredMixin, FormMixin, ProcessFormView):
    '''添加购物车'''
    form_class = BaykeShopCartAddForm

    def form_valid(self, form):
        BaykeShopCart.add_cart(
            self.request,
            form.cleaned_data['sku_id'], 
            form.cleaned_data['num']
        )
        return JsonResponse(
            {
                'code': 200, 
                'msg': _('添加购物车成功'),
                'data': {
                    'cart_count': BaykeShopCart.get_cart_count(self.request.user),
                    'cart_total_price': BaykeShopCart.get_cart_total_price(self.request.user)
                }
            }, 
            json_dumps_params={'ensure_ascii': False}
        )
    
    def form_invalid(self, form):
        return JsonResponse(
            {'code': 400, 'msg': form.errors}, 
            json_dumps_params={'ensure_ascii': False}
        )
    
    def handle_no_permission(self):
        return JsonResponse(
            { 'code': 401, 'msg': _('请登录后继续操作') }, 
            json_dumps_params={'ensure_ascii': False}
        )
    

class BaykeShopCartChangeView(BaykeShopCartAddView):
    '''购物车数量修改'''
    def form_valid(self, form):
        BaykeShopCart.change_num(
            self.request,
            form.cleaned_data['sku_id'], 
            form.cleaned_data['num']
        )
        return JsonResponse(
            {
                'code': 200, 
                'msg': _('修改成功'),
            }, 
            json_dumps_params={'ensure_ascii': False}
        )


class BaykeShopCartDelView(BaykeShopCartAddView):
    def form_valid(self, form):
        BaykeShopCart.del_cart(
            self.request,
            form.cleaned_data['sku_id']
        )
        return JsonResponse(
            {
                'code': 200, 
                'msg': _('删除成功'),
            }, 
            json_dumps_params={'ensure_ascii': False}
        )