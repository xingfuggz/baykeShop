from django_filters import rest_framework as filters

from . import models


class ArticleFilter(filters.FilterSet):
    
    class Meta:
        model = models.BaykeArticle
        fields = ('category__name',)