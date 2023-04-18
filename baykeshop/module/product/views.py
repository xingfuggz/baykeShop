from django.core.cache import cache

from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.filters import SearchFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from baykeshop.models import product
from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.public.serializers import BaykeGoodsSerializer
from baykeshop.public.pagination import PageNumberPagination
from baykeshop.module.product.filter import BaykeGoodsFilter, BaykeGoodsOrderingFilter
from baykeshop.module.product.serializers import BaykeCategorySerializer, BaykeGoodsDetailSerializer


class BaykeGoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 全部商品 """
    queryset = product.BaykeGoods.objects.all()
    serializer_class = BaykeGoodsSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    pagination_class = PageNumberPagination
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = [DjangoFilterBackend, SearchFilter, BaykeGoodsOrderingFilter]
    filterset_class = BaykeGoodsFilter
    template_name = "baykeshop/product/goods.html"
    search_fields = ("title", "desc", "keywords", "content")
    ordering_fields = ('baykeproduct__price', 'baykeproduct__sales', 'add_date',)
     
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs) 
        cates = BaykeCategorySerializer(self.get_parent_category_queryset(), many=True)
        sub_cates = BaykeCategorySerializer(self.get_sub_cates(), many=True)

        response.data = {
            'goods': response.data,
            'cates': cates.data,
            'sub_cates': sub_cates.data,
            'query': request.query_params
        }
        return response
    
    def get_queryset(self):
        return super().get_queryset()

    def get_category_queryset(self):
        return product.BaykeCategory.objects.all().order_by('-add_date')
    
    def get_parent_category_queryset(self):
        return self.get_category_queryset().filter(parent__isnull=True)
    
    def get_sub_cates(self):
        query = self.request.query_params
        if query.get('categorys'):
            cate = product.BaykeCategory.objects.get(id=int(query.get('categorys')))
            if cate.parent is None:
                return self.get_category_queryset().filter(parent__id=int(query.get('categorys')))
            else:
                return self.get_category_queryset().filter(parent__id=cate.parent.id)
        elif not query.get('categorys'):
            return self.get_category_queryset().filter(parent=self.get_parent_category_queryset().first())

             
class BaykeGoodsDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ 商品详情页接口 """
    queryset = product.BaykeGoods.objects.all()
    serializer_class = BaykeGoodsDetailSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "baykeshop/product/detail.html"


class BaykeCacheGoodsAPIview(APIView):
    """ 缓存商品接口 """
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        message = ""
        code = ""
        if request.data.get('action') == 'cartBuy':
            cache.set(f'{request.user.id}cartBuy', request.data, None)
            message = "缓存成功"
            code = status.HTTP_201_CREATED
        elif request.data.get('action') == 'nowBuy':
            message = "缓存成功"
            code = status.HTTP_201_CREATED
        else:
            message = "缓存失败"
            code = status.HTTP_400_BAD_REQUEST
        return Response({'message': message}, status=code)