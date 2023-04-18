from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializer
from . import page
from . import filters

class ArticleMixin:
    
    def tags_serializer(self):
        return serializer.BaykeArticleTagSerializer(models.BaykeArticleTag.objects.all(), many=True)

    def cates_serializer(self):
        return serializer.BaykeArticleCategorySerializer(models.BaykeArticleCategory.objects.all(), many=True)
        

class BaykeArticleViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, ArticleMixin, viewsets.GenericViewSet):
    """ 商城资讯列表 """
    queryset = models.BaykeArticle.objects.all()
    serializer_class = serializer.BaykeArticleSerializer
    pagination_class = page.PageNumberPagination
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = [DjangoFilterBackend,]
    filterset_class = filters.ArticleFilter
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.template_name = "baykeshop/article/list.html"
        response.data['tags'] = self.tags_serializer().data
        response.data['cates'] = self.cates_serializer().data
        return response
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.template_name = "baykeshop/article/detail.html"
        response.data['tags'] = self.tags_serializer().data
        response.data['cates'] = self.cates_serializer().data
        return response
