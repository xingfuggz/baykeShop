from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter


from baykeshop.models import product


class BaykeGoodsFilter(filters.FilterSet):
    
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


class BaykeGoodsOrderingFilter(OrderingFilter):
    
    def filter_queryset(self, request, queryset, view):
        """ 跨模型筛选会有重复sku，这里操作去重 """
        result = []
        for q in super().filter_queryset(request, queryset, view):
            if q not in result:
                result.append(q)
        return result