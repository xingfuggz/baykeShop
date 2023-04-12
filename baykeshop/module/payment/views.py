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


class ConfirmOrderAPIView(GenericAPIView):
    """ 订单确认 """
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = BaykeShopAddressSerializer
    
    def get(self, request, *args, **kwargs):
        context = {'address': self.address_datas}
        return Response(context, template_name="baykeshop/payment/confirm_order.html")
    
    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response({'message': '缓存成功'}, status=status.HTTP_201_CREATED)
    
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