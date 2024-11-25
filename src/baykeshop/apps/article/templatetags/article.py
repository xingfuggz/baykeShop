from django.template import Library
from baykeshop.apps.article.models import (
    BaykeArticleCategory, BaykeArticleTags, BaykeArticle
)

register = Library()

@register.simple_tag(name='article_category_list')
def category_list():
    """获取分类列表"""
    return BaykeArticleCategory.objects.filter(is_show=True, parent__isnull=True)


@register.simple_tag(name='article_tag_list')
def tags_list():
    """获取标签列表"""
    return BaykeArticleTags.objects.all()


@register.simple_tag(name='tags_article_list')
def tags_article_list(article:BaykeArticle):
    """获取标签文章列表"""
    return BaykeArticle.objects.filter(tags__in=article.tags.all()).distinct()
