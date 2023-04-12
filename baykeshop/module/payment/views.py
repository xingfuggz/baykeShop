from rest_framework import mixins
from rest_framework import viewsets
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
        return Response({}, template_name="baykeshop/payment/confirm_order.html")
    
    def get_queryset(self):
        return BaykeShopAddress.objects.filter(owner=self.request.user)