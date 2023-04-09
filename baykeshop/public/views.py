from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from baykeshop.models import public
from baykeshop.models import product
from baykeshop.public.serializers import (
    HomeBaykeCategorySerializer, BaykeBannerSerializer
)


class HomeView(GenericAPIView):
    """ 首页 """
    queryset = product.BaykeCategory.objects.filter(parent__isnull=True, is_nav=True)
    serializer_class = HomeBaykeCategorySerializer
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    
    def get(self, request):
        datas = {
            "cates": self.get_serializer().data,
            "banners": self.get_banners_serializer().data
        }
        return Response(datas, template_name="baykeshop/index.html")
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(self.get_queryset(), many=True)
    
    def get_banners_serializer(self, *args, **kwargs):
        return BaykeBannerSerializer(public.BaykeBanner.objects.all(), many=True)
        
    
    

