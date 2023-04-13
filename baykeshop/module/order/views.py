from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.module.order.models import BaykeOrderInfo, BaykeOrderGoods
from baykeshop.module.order.serializer import BaykeOrderInfoSerializer, BaykeOrderGoodsSerializer



class BaykeOrderInfoViewset(mixins.ListModelMixin, 
                            mixins.RetrieveModelMixin, 
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    # renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = BaykeOrderInfoSerializer
    
    def get_queryset(self):
        return BaykeOrderInfo.objects.filter(owner=self.request.user)