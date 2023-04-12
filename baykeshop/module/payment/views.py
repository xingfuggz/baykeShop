from django.core.cache import cache

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from baykeshop.module.user.models import BaykeShopAddress
from baykeshop.module.user.serializers import BaykeShopAddressSerializer
from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.module.cart.serializers import CartBaykeProductSerializer
from baykeshop.module.product.models import BaykeProduct



class ConfirmOrderAPIView(GenericAPIView):
    """ 订单确认 """
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = BaykeShopAddressSerializer
    
    def get(self, request, *args, **kwargs):
        context = {
            'address': self.address_datas,
            **self.get_goods()
        }
        return Response(context, template_name="baykeshop/payment/confirm_order.html")
    
    def post(self, request, *args, **kwargs):
        # 缓存
        if request.data.get('action') == 'nowBuy':
            cache.set(f'{request.user.id}goods', request.data)
        return Response({'message': '缓存成功'}, status=status.HTTP_201_CREATED)
    
    def get_goods(self):
        query = self.request.query_params
        cache_data = None
        serializer = {}
        action = None
        # 判断是从哪里跳转到该页面的
        if query.get('action') == 'nowBuy':
            cache_data = cache.get(f'{self.request.user.id}goods')
            serializer['goods'] = CartBaykeProductSerializer(BaykeProduct.objects.filter(id=cache_data.get('sku')), many=True).data
            serializer['num'] = cache_data.get('num', 0)
            serializer['action'] = query.get('action')
        return serializer
        
    
    @property
    def address_datas(self):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data
    
    def get_queryset(self):
        return BaykeShopAddress.objects.filter(owner=self.request.user)