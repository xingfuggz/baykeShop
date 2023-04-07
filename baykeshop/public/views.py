from django.utils.safestring import mark_safe

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from baykeshop.models import public
from baykeshop.models import product
# from baykeshop.views import BaykeBannerViewMixin
from baykeshop.models.context import BaykeModelContext
from baykeshop.public.serializers import HomeBaykeCategorySerializer


class HomeView(GenericAPIView):
    """ 首页 """
    queryset = product.BaykeCategory.objects.filter(parent__isnull=True, is_nav=True)
    serializer_class = HomeBaykeCategorySerializer
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    
    def get(self, request):
        # json和html数据中都要返回的数据
        datas = {
            "cates": self.get_serializer().data,
            **BaykeModelContext(public.BaykeBanner, context_name="banners").context()
        }
        return Response(datas, template_name="baykeshop/index.html")
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(self.get_queryset(), many=True)

        
    
    

