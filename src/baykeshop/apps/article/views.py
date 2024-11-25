'''
@file            :views.py
@Description     :文章视图
@Date            :2024/11/03 20:10:48
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''
from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from django.views.generic import ListView, MonthArchiveView
from django.views.generic.detail import DetailView, SingleObjectMixin
# Create your views here.
from baykeshop.apps.core.models import Visit
from .models import BaykeArticle, BaykeArticleCategory, BaykeArticleTags


class ArticleBaseView:
    """ 文章视图基类 """
    def get_article_list(self):
        """ 文章列表 """
        return BaykeArticle.objects.filter(is_show=True)
    
    def get_category_list(self):
        """ 分类列表 """
        return BaykeArticleCategory.objects.filter(is_show=True)
    
    def get_tag_list(self):
        """ 标签列表 """
        return BaykeArticleTags.objects.all()
    
    def get_archive_list(self):
        """ 归档列表 """
        return BaykeArticle.objects.filter(is_show=True).datetimes('create_time', 'month')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archive_list'] = self.get_archive_list()
        return context
    

class ArticleListView(ArticleBaseView, ListView):
    """ 文章列表视图 """
    template_name = 'article/list.html'
    paginate_by = 20

    def get_queryset(self):
        """ 重写查询集 """
        return self.get_article_list()
    

class ArticleDetailView(ArticleBaseView, DetailView):
    """ 文章详情视图 """
    template_name = 'article/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        """ 重写get方法 """
        response = super().get(request, *args, **kwargs)
        Visit.objects.create_pv_uv(request, self.get_object())
        return response

    def get_queryset(self) -> QuerySet[Any]:
        return self.get_article_list()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visit'] = self.get_visit_count()
        print(context['visit'])
        return context
    
    def get_visit_count(self):
        return Visit.objects.get_uv_pv_count(self.get_object())


class ArticleCategoryView(ArticleBaseView, SingleObjectMixin, ListView):
    """ 分类列表页 """
    template_name = 'article/list.html'
    paginate_by = 10
    paginate_orphans = 1
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.get_category_list())
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.object.baykearticle_set.filter(is_show=True)
    

class ArticleAuthorListView(ArticleBaseView, SingleObjectMixin, ListView):
    """ 作者文章列表页 """
    template_name = 'article/list.html'
    paginate_by = 10
    paginate_orphans = 1
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=get_user_model().objects.all())
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.object.baykearticle_set.filter(is_show=True)
    

class ArticleTagListView(ArticleBaseView, SingleObjectMixin, ListView):
    """ 标签文章列表页 """
    template_name = 'article/list.html'
    paginate_by = 10
    paginate_orphans = 1
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.get_tag_list())
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.object.baykearticle_set.filter(is_show=True)


class ArchiveListView(ArticleBaseView, MonthArchiveView):
    """ 归档列表页 """
    template_name = 'article/list.html'
    paginate_by = 10
    paginate_orphans = 1
    date_field = "create_time"
    allow_future = False
    month_format = "%m"

    def get_queryset(self):
        return self.get_article_list()