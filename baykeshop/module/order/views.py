from django.core.cache import cache

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.module.cart.models import BaykeShopingCart
from baykeshop.module.order.models import BaykeOrderInfo, BaykeOrderGoods
from baykeshop.module.order.serializer import BaykeOrderInfoSerializer, BaykeOrderGoodsSerializer
from baykeshop.module.payment.computed import computed_pay


class BaykeOrderInfoViewset(mixins.ListModelMixin, 
                            mixins.RetrieveModelMixin, 
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    # renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = BaykeOrderInfoSerializer
    
    def get_queryset(self):
        return BaykeOrderInfo.objects.filter(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data['total_amount'] = self.confirm(data['action'], data['sku'], data['num']).get_total_amount()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()
        data = self.request.data
        if data.get('action') == 'cartBuy':
            carts = cache.get(f"{self.request.user.id}cartBuy")
            carts_ids = [int(cart['id']) for cart in carts['skus']]
            # 删除购物车
            BaykeShopingCart.objects.filter(owner=self.request.user, id__in=carts_ids).delete()
            # 删除缓存
            cache.delete(f"{self.request.user.id}cartBuy")
            
    def confirm(self, action, sku, num):
        return computed_pay(self.request, action, sku, num)