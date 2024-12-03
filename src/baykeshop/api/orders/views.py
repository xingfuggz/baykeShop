from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import BaykeShopOrdersCreateSerializer


class BaykeShopOrdersGenericAPIView(generics.GenericAPIView):
    """ 创建订单 """
    serializer_class = BaykeShopOrdersCreateSerializer
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        messages.success(request, _('下单成功'))
        return Response(serializer.data)

    
        