from django.db.utils import IntegrityError
from django.db.models import F
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer


from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.module.cart.serializers import (
    BaykeShopingCartSerializer, CartBaykeShopingListSerializer
)
from baykeshop.module.cart.models import BaykeShopingCart


class BaykeshopingCartViewSet(viewsets.ModelViewSet):
    
    serializer_class = BaykeShopingCartSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get_queryset(self):
        return BaykeShopingCart.objects.filter(owner=self.request.user, sku__is_release=True)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CartBaykeShopingListSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.template_name = "baykeshop/cart/list.html"
        return response

    def perform_create(self, serializer):
        try:
            super().perform_create(serializer)
        except IntegrityError:
            self.get_queryset().filter(
                    sku__id=int(serializer.data['sku'])
                ).update(num=F('num')+serializer.data['num'])
            