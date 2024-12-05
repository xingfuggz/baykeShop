from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from rest_framework import mixins, viewsets
from rest_framework import authentication
from rest_framework import permissions

from baykeshop.contrib.shop.models import BaykeShopOrders

from .serializers import BaykeShopOrdersCreateSerializer


class BaykeShopOrdersViewSet(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin, 
                             viewsets.GenericViewSet):
    """ 创建订单 """
    queryset = BaykeShopOrders.objects.all()
    serializer_class = BaykeShopOrdersCreateSerializer
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'order_sn'
    lookup_field = 'order_sn'
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        messages.success(self.request, _('订单删除成功'))

