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
from django_filters.rest_framework import DjangoFilterBackend

from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.module.order.filters import BaykeOrderInfoFilter
from baykeshop.module.order.models import BaykeOrderInfo, BaykeOrderGoods
from baykeshop.module.order.serializer import (
    BaykeOrderInfoSerializer, BaykeOrderInfoListSerializer, BaykeOrderGoodsSerializer
)
from baykeshop.module.order.page import OrderInfoPageNumberPagination
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = BaykeOrderInfoFilter
    pagination_class = OrderInfoPageNumberPagination
    
    def get_queryset(self):
        return BaykeOrderInfo.objects.filter(owner=self.request.user).order_by('-add_date')
    
    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = BaykeOrderInfoListSerializer
        # elif self.action == 'commentgoods':
        #     from baykeshop.module.comment.serializer import BaykeOrderInfoCommentsSerializer
        #     self.serializer_class = BaykeOrderInfoCommentsSerializer
            
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'orders': response.data}, template_name="baykeshop/user/orders.html")
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.template_name = "baykeshop/order/detail.html"
        return response
    
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
        """余额订单结算接口
        @api: /order/{order_sn}/balance/
        @method: get
        @params: {}
        @auth: True
        @return: 成功 status=200   失败 status=400
        """
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
        return Response(
            {'order': serializer.data, 'message': message}, 
            template_name="baykeshop/payment/alipay_notfiy.html", 
            status=code
        )
    
    @action(detail=True, methods=['post'])
    def confirmorder(self, request, order_sn=None):
        """确认收货接口
        @api: /order/{order_sn}/confirmorder/ 
        @method: post
        @data: {}
        @return {'message': '已确认收货', 'order_sn': order_sn}
        """
        self.get_queryset().filter(order_sn=order_sn).update(pay_status=4)
        return Response({'message': '已确认收货', 'order_sn': order_sn})
    
    @action(detail=True, methods=['get', 'post'])
    def commentgoods(self, request, order_sn=None, *args, **kwargs):
        """ 发表评价接口 """
        
        # 评价表单
        if request.method == "GET":
            response = super().retrieve(request, *args, **kwargs)
            response.template_name = "baykeshop/user/comment.html"
            return response
        
        # 发表评价
        if request.method == "POST":
            message = "评价成功"
            code = status.HTTP_201_CREATED
            from django.contrib.contenttypes.models import ContentType
            from baykeshop.module.order.models import BaykeOrderGoods
            from baykeshop.module.comment.models import BaykeOrderInfoComments
            
            if not request.data or not request.data.get('content'):
                message = "评价内容不能为空！"
                code = status.HTTP_400_BAD_REQUEST
                return Response({'message': message}, status=code)
            
            # 查询出当前评论的商品
            order_goods = BaykeOrderGoods.objects.filter(
                id=int(request.data['object_id']), 
                is_commented=False, 
                orderinfo__owner=request.user
            )
            
            # 判断是否已经评价过，禁止重复评价
            if not order_goods.exists():
                message = "该商品已经评价，无需重复评价！"
                code = status.HTTP_400_BAD_REQUEST
                return Response({'message': message}, status=code)
            
            # 获取关联的评论模型
            content_type = ContentType.objects.get_for_model(BaykeOrderGoods)
            
            # 增加一条评论
            BaykeOrderInfoComments.objects.create(
                owner=request.user,
                content_type=content_type,
                **request.data
            )
            # 标记为已评价
            order_goods.update(is_commented=True)
            
            # 修改订单状态
            order = self.get_object()
            order.pay_status = 5
            order.save()
    
            return Response({'message': message}, status=code)
    


class BaykeOrderGoodsViewset(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = BaykeOrderGoodsSerializer 
    
    def get_queryset(self):
        return BaykeOrderGoods.objects.filter(orderinfo__owner=self.request.user)
    