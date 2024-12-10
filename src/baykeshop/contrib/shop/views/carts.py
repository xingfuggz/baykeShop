import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from baykeshop.contrib.shop.models import BaykeShopCarts

User = get_user_model()


class BaykeShopCartsListView(LoginRequiredMixin, ListView):
    """ 购物车列表 """
    template_name = 'baykeshop/shop/carts.html'
    context_object_name = 'carts_list'
    extra_context = {
        'title': _('购物车'),
    }

    def get_queryset(self):
        queryset = BaykeShopCarts.objects.filter(user=self.request.user).order_by('-created_time')
        queryset = list(queryset.values(
            'id', 'total_price', 'name', 'specs', 'image_url', 'sku_id',
            'sku__price', 'sku__stock', 'sku__sales', 'quantity'
        ))
        for item in queryset:
            item['specs'] = json.loads(item['specs'])
            item['total_price'] = round(item['total_price'], 2)
        return queryset

