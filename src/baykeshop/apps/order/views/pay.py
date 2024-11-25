from django.db import models
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseRedirect, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your views here.
from alipay.aop.api.util.SignatureUtils import verify_with_rsa

from baykeshop.apps.core.pay import alipay
from baykeshop.apps.shop.models import BaykeShopSKU, BaykeShopCart
from baykeshop.apps.order.models import BaykeShopOrder, BaykeShopOrderLog


class CashRegisterView(LoginRequiredMixin, TemplateView):
    """ 收银台 """
    template_name = 'order/cash.html'
    login_url = reverse_lazy('user:login')
    sku_queryset = None
    cart_queryset = None
    
    def get(self, request, *args, **kwargs):
        sku_ids = self.request.GET.get('sku_ids')
        if not sku_ids:
            return HttpResponseNotFound(content='参数错误')
        self.get_product_queryset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_queryset'] = self.cart_queryset
        context['sku_queryset'] = self.sku_queryset
        context['total_price'] = self.get_total_price()
        context['nums'] = (self.cart_queryset.count() if self.cart_queryset else None) or self.request.GET.get('count', 1)
        context['source'] = self.request.GET.get('source', 'detail')
        context['title'] = _('订单提交')
        return context
    
    def get_product_queryset(self):
        """ 获取要结算的商品数据 
        这个数据主要有两个来源
            1.商品详情页的理解购买按钮点击传递
            2.购物车页面去结算按钮点击传递
            @param: sku_ids 商品id列表
            @param: source 订单来源 1.详情页(detail) 2.购物车(cart)
            @param: count 购买数量, 这个主要是详情页来源必须携带，购物车页面直接去查询购物车数据获取数量
        """
        count = self.request.GET.get('count', 1)
        source = self.request.GET.get('source', 'detail')
        sku_ids = self.request.GET.get('sku_ids', '')
        sku_ids = [int(i) for i in sku_ids.split(',') if i]
        if source == 'detail' and len(sku_ids) == 1:
            self.sku_queryset = BaykeShopSKU.objects.filter(id__in=sku_ids).alias(
                total_price=models.ExpressionWrapper(
                    models.F('price') * int(count),
                    output_field=models.DecimalField()
                )
            ).annotate(total_price=models.F('total_price'))
        elif source == 'cart' and len(sku_ids) >= 1:
            self.cart_queryset = BaykeShopCart.get_cart_queryset(self.request.user).filter(sku_id__in=sku_ids)

    def get_total_price(self):
        """ 获取订单总金额 """
        total_price = 0
        if self.cart_queryset:
            total_price = sum(self.cart_queryset.values_list('total_price', flat=True))
        elif self.sku_queryset:
            total_price = self.sku_queryset.values_list('total_price', flat=True).first()
        return total_price
    

class OrderPayView(LoginRequiredMixin, DetailView):
    """ 订单支付 """
    template_name = 'order/pay.html'
    login_url = reverse_lazy('user:login')
    model = BaykeShopOrder
    slug_field = 'order_sn'
    slug_url_kwarg = 'order_sn'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def alipay(self):
        """ 支付宝支付 """
        res = alipay.pay(
            order_sn=self.object.order_sn,
            total_price=str(self.object.pay_price),
            subject=self.object.order_sn,
            return_url=self.request.build_absolute_uri(reverse('order:order-alipay')),
            notify_url=self.request.build_absolute_uri(reverse('order:order-alipay'))
        )
        return res
   
    def post(self, request, *args, **kwargs):
        """ 订单支付 """
        self.object = self.get_object()
        pay_type = request.POST.get('pay_type', 0)
        status = BaykeShopOrder.OrderStatus.WAIT_PAY
        # 判断订单状态是否为待支付
        if self.object.status != status:
            return JsonResponse({'code': 400, 'msg': '该订单状态不支持支付哦！'})

        # 支付宝支付
        if int(pay_type) == 0:
            url = self.alipay()
            return JsonResponse({ 'code': 200, 'data': url }, 
                json_dumps_params={'ensure_ascii': False}
            )
        # 微信支付
        if int(pay_type) == 1:
            return JsonResponse({'code': 200, 'msg': '正在开发微信支付...'})
        # 货到付款
        if int(pay_type) == 2:
            self.object.status = BaykeShopOrder.OrderStatus.WAIT_VERIFY
            self.object.pay_type = BaykeShopOrder.PayType.OTHER
            self.object.save()
            BaykeShopOrderLog.create_log(
                self.object, 
                '货到付款', 
                self.request.user
            )
            return JsonResponse({'code': 200, 'msg': '已完成，稍后会有工作人员联系你哦！'})
        return JsonResponse({'code': 400, 'msg': '支付类型错误'})


class AlipayCallBackVerifySignMixin:
    """ 支付宝支付回调，验签 """
    
    def has_verify_sign(self, data):
        """ 验签
        data是从请求中获得的字典数据，携带 sign和sign_type
        """
        sign = data.pop('sign')
        sign_type = data.pop('sign_type')
        alipay_public_key = alipay.get_alipay_public_key()
        print(alipay_public_key)
        # 去除sign和sign_type参数之后进行升序排列，拼装请求参数用支付宝公钥进行验签
        message='&'.join([f"{k}={v}" for k, v in dict(sorted(data.items(), key=lambda d: d[0], reverse=False)).items()])
        flag = verify_with_rsa(alipay_public_key, message.encode('UTF-8','strict'), sign)
        return flag


class AlipayCallbackView(AlipayCallBackVerifySignMixin, View):
    """ 支付宝支付结果通知 """
    def get(self, request, *args, **kwargs):
        """ 支付宝同步通知 """
        data = request.GET.dict()
        success = self.has_verify_sign(data)
        order_sn = data.get('out_trade_no')
        if success:
            order = BaykeShopOrder.objects.filter(order_sn=order_sn).first()
            if order:
                order.pay_time = timezone.now()
                order.pay_id = data.get('trade_no')
                order.pay_type = BaykeShopOrder.PayType.ALIPAY
                order.status = BaykeShopOrder.OrderStatus.WAIT_DELIVER
                order.save()
            return HttpResponseRedirect(reverse('order:order-detail', kwargs={'order_sn': order_sn}))
        return HttpResponse('success')
    
    def post(self, request, *args, **kwargs):
        """ 支付宝异步通知 """
        data = request.POST.dict()
        order_sn = data.get('out_trade_no')
        success = self.has_verify_sign(data)
        if success:
            order = BaykeShopOrder.objects.filter(order_sn=order_sn).first()
            if order:
                order.pay_time = timezone.now()
                order.pay_id = data.get('trade_no')
                order.pay_type = BaykeShopOrder.PayType.ALIPAY
                order.status = BaykeShopOrder.OrderStatus.WAIT_DELIVER
                order.save()
            return HttpResponse('success')