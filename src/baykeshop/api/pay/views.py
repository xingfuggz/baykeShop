from rest_framework import mixins, viewsets
from rest_framework import authentication
from rest_framework import permissions

from baykeshop.contrib.shop.models import BaykeShopOrders
from .serializers import BaykeShopOrdersPaySerializer


class BaykeShopOrdersPayView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    支付订单
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = BaykeShopOrders.objects.all()
    serializer_class = BaykeShopOrdersPaySerializer
    lookup_field = 'order_sn'
    lookup_url_kwarg = 'order_sn'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)