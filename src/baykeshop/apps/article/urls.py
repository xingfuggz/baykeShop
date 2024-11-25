'''
@file            :urls.py
@Description     :urls配置(对应模版系统视图)
@Date            :2024/11/03 19:59:29
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('list/', views.ArticleListView.as_view(), name='article_list'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('category/<int:pk>/', views.ArticleCategoryView.as_view(), name='article_category'),
    path('author/<int:pk>/', views.ArticleAuthorListView.as_view(), name='article_author'),
    path('tag/<int:pk>/', views.ArticleTagListView.as_view(), name='article_tag'),
    path('archive/<int:year>/<int:month>/', views.ArchiveListView.as_view(), name='archive_list'),
]