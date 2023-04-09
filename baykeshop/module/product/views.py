from django.db.models import Q
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.renderers import JSONRenderer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from baykeshop.models import product
from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.public.serializers import BaykeGoodsSerializer, HomeBaykeCategorySerializer
from baykeshop.module.product.filter import BaykeProductFilter
from baykeshop.module.product.serializers import BaykeCategorySerializer


class BaykeGoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 全部商品 """
    queryset = product.BaykeGoods.objects.all()
    serializer_class = BaykeGoodsSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    pagination_class = pagination.PageNumberPagination
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BaykeProductFilter
    template_name = "baykeshop/product/goods.html"
    search_fields = ("title", "desc", "keywords", "content")
    ordering_fields = ('baykeproduct__price', 'add_date')
    
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
        
        