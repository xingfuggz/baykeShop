from rest_framework import mixins, viewsets
from rest_framework import authentication, permissions
from baykeshop.contrib.shop.models import BaykeShopOrdersComment
from .serializers import BaykeShopOrdersCommentSerializer



class BaykeShopOrdersCommentViewSet(mixins.CreateModelMixin, 
                                    viewsets.GenericViewSet):
    """订单评论"""
    queryset = BaykeShopOrdersComment.objects.all()
    serializer_class = BaykeShopOrdersCommentSerializer
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    