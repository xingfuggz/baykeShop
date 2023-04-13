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
        code = status.HTTP_200_OK
        context = {
            'address': self.address_datas,
            'skus': pay.get_skus(),
            'pay': pay.computed,
            'is_pay': pay.validate
        }
        if not pay.validate:
            context['address'] = []
            context['error'] = "不是有效地址！"
            code = status.HTTP_404_NOT_FOUND
        return Response(context, template_name="baykeshop/payment/confirm_order.html", status=code)
          
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