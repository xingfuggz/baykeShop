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
from baykeshop.module.payment.computed import NowBuyComputed, CartBuyComputed



class ConfirmOrderAPIView(GenericAPIView):
    """ 订单确认 """
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = BaykeShopAddressSerializer
    
    def get(self, request, *args, **kwargs):
        query = request.query_params
        code = status.HTTP_200_OK
        pay = None
        if query.get('action') == 'nowBuy':
            pay = NowBuyComputed(request, int(query.get('sku')), query.get('num'))
        elif query.get('action') == 'cartBuy':
            pay = CartBuyComputed(request)
        context = {'address': self.address_datas,'skus': [], 'is_pay': False, 'pay': None,'query': query}
        if pay:
            context['skus'] = pay.get_skus()
            context['pay'] = pay.computed()
            context['is_pay'] = pay.validate
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