from baykeshop.module.order.models import BaykeOrderInfo

from django_filters import rest_framework as filters


class BaykeOrderInfoFilter(filters.FilterSet):
    
    class Meta:
        model = BaykeOrderInfo
        fields = ('pay_status',)