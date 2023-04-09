from django_filters import rest_framework as filters

from baykeshop.models import product


class BaykeProductFilter(filters.FilterSet):
    
    class Meta:
        model = product.BaykeGoods
        fields = ('categorys',)

    def filter_queryset(self, queryset):
        """ 按分类筛选 """
        query = self.request.query_params
        if query and query.get('categorys'):
            cate = product.BaykeCategory.objects.get(id=int(query.get('categorys')))
            if cate.parent is None:
                return queryset.filter(categorys__in=cate.baykecategory_set.all())
        return super().filter_queryset(queryset)
