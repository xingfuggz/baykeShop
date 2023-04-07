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


class HomeView(GenericAPIView):
    """ 首页 """
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    
    def get(self, request):
        # json和html数据中都要返回的数据
        datas = {
            'cates':list(self.get_queryset()), 
            **BaykeModelContext(public.BaykeBanner, context_name="banners").context()
        }
        return Response(datas, template_name="baykeshop/index.html")
    
    def get_queryset(self):
        parent_cates = product.BaykeCategory.objects.filter(parent__isnull=True, is_nav=True).values()
        for parent in parent_cates:
            parent['products'] = list(product.BaykeGoods.objects.filter(
                categorys__in=parent.baykecategory_set.all()).distinct().values())
        return parent_cates
    
    

