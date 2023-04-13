from decimal import Decimal
from django.core.cache import cache


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
from baykeshop.module.cart.models import BaykeShopingCart
from baykeshop.module.cart.serializers import CartBaykeProductSerializer, CartBaykeShopingListSerializer
from baykeshop.module.product.models import BaykeProduct
from baykeshop.module.payment.computed import ComputedPayMent



class ConfirmOrderAPIView(GenericAPIView):
    """ 订单确认 """
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = BaykeShopAddressSerializer
    
    def get(self, request, *args, **kwargs):
        
        pay = ComputedPayMent(request)
        pay.get_serializer
        context = {
            'address': self.address_datas,
            **self.get_goods()
        }
        return Response(context, template_name="baykeshop/payment/confirm_order.html")
    
    def get_goods(self):
        serializer = {}
        num = 0         # 商品总数量
        total = 0       # 商品总价
        freight = 0     # 运费
        total_amount = 0
        cache_data = (
            cache.get(f'{self.request.user.id}nowBuy{self.request.query_params.get("sku")}') or
            cache.get(f'{self.request.user.id}cartBuy')
        )
        # 判断是从哪里跳转到该页面的
        if cache_data.get('action') == 'nowBuy':
            serializer['sku'] = CartBaykeProductSerializer(BaykeProduct.objects.filter(id=cache_data.get('sku')).first()).data
            num = cache_data.get('num', 0)
            total = serializer['sku']['price'] * cache_data.get('num', 0)
            freight = Decimal(serializer['sku']['goods']['freight'])
            total_amount = Decimal(total) + Decimal(freight)
            
            serializer['num'] = num
            serializer['totalprice'] = total
            serializer['action'] = cache_data.get('action')
            serializer['freight'] = freight
            serializer['total_amount'] =  total_amount
            
        elif cache_data.get('action') == 'cartBuy':
            cart_ids = [cart['id'] for cart in cache_data.get('skus', []) ]
            serializer['carts'] = CartBaykeShopingListSerializer(BaykeShopingCart.objects.filter(id__in=cart_ids), many=True).data
            serializer['action'] = cache_data.get('action')
            for cart in serializer['carts']:
                # 该商品的总价
                cart['sku']['totalprice'] = int(cart['num']) * Decimal(cart['sku']['price'])
                # 计算所有商品的总价
                total += cart['sku']['totalprice']
                # 总数量
                num += cart['num']
                # 计算运费
                freight += Decimal(cart['sku']['goods']['freight'])
            # 商品数量
            serializer['num'] = num
            # 运费
            serializer['freight'] = freight
            # 不含运费的总价
            serializer['totalprice'] = total
            # 含运费的总价
            total_amount = total + freight
            serializer['total_amount'] = total_amount
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