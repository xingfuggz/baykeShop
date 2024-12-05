from django.urls import path

from . import views

app_name = 'article'

urlpatterns = [
    # 文章列表
    path('', views.BaykeArticleContentListView.as_view(), name='list'),
    # 文章详情
    path('<int:pk>/', views.BaykeArticleContentDetailView.as_view(), name='detail'),
    # 分类文章列表
    path('category/<int:pk>/', views.BaykeArticleCategoryListView.as_view(), name='category'),
    # 标签文章列表
    path('tags/<int:pk>/', views.BaykeArticleTagsListView.as_view(), name='tags'),
    # 搜索文章列表
    path('search/', views.BaykeArticleSearchView.as_view(), name='search'),
    # 归档文章列表
    path('archive/<int:year>/<int:month>/', views.BaykeArticleArchiveView.as_view(), name='archive'),
    # 用户文章列表
    path('user/<int:pk>/', views.BaykeArticleUserListView.as_view(), name='user'),
]


