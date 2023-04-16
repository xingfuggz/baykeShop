from django.core.cache import cache
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.module.cart.models import BaykeShopingCart
from baykeshop.module.order.models import BaykeOrderInfo, BaykeOrderGoods
from baykeshop.module.order.serializer import BaykeOrderInfoSerializer
from baykeshop.module.payment.computed import computed_pay


class BaykeOrderInfoViewset(mixins.ListModelMixin, 
                            mixins.RetrieveModelMixin, 
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = BaykeOrderInfoSerializer
    lookup_field = 'order_sn'
    
    def get_queryset(self):
        return BaykeOrderInfo.objects.filter(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.data['total_amount'] = self.confirm.get_total_amount()
        response = super().create(request, *args, **kwargs)
        return response
    
    def perform_create(self, serializer):
        orderinfo = serializer.save()
        carts = self.confirm.cache_cart
        # 保存订单关联商品
        self.confirm.save_order_goods(orderinfo)
        if carts:
            # 如果为购物车商品还需清理购物车
            self.confirm.get_queryset().delete()
            # 清理购物车缓存
            cache.delete(f"{self.request.user.id}cartBuy")
    
    @property
    def confirm(self):
        data = {'action': 'cartBuy', 'sku':None, 'num': 1}
        if self.request.method == 'GET':
            data = self.request.query_params
        else:
            data = self.request.data
        return computed_pay(self.request, data['action'], data['sku'], data['num'])
    
    @action(detail=True, methods=['get'])
    def pay(self, request, order_sn=None):
        # 订单结算视图
        orderinfo = self.get_object()
        serializer = self.get_serializer(orderinfo)
        return Response({'order': serializer.data}, template_name="baykeshop/payment/pay.html")
    
    @action(detail=True, methods=['get'])
    def balance(self, request, order_sn=None):
        # 订单结算视图
        orderinfo = self.get_object()
        serializer = self.get_serializer(orderinfo)
        from django.utils import timezone
        from django.db.models import F
        from baykeshop.module.user.models import BaykeUserInfo, BaykeUserBalanceLog
        userinfo = BaykeUserInfo.objects.filter(owner=request.user)

        code = status.HTTP_200_OK
        message = ""
       
        is_updates = [
            userinfo.exists(), 
            (userinfo.first().balance > orderinfo.total_amount), 
            orderinfo.pay_status == 1
        ]
        if all(is_updates):
            userinfo.update(balance=F('balance')-orderinfo.total_amount)
            orderinfo.pay_status = 2
            orderinfo.trade_sn = f"YE{orderinfo.order_sn}"
            orderinfo.pay_method = 4
            orderinfo.pay_time=timezone.now()
            orderinfo.save()
            
            # 记录余额变动日志
            BaykeUserBalanceLog.objects.create(
                owner=request.user, 
                amount=orderinfo.total_amount, 
                change_status=2,
                change_way=3
            )
        else:
            code = status.HTTP_400_BAD_REQUEST
            message = "余额不足！"
        return Response({'order': serializer.data, 'message': message}, template_name="baykeshop/payment/alipay_notfiy.html", status=code)
        