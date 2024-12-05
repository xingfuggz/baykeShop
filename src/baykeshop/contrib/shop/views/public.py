from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from baykeshop.contrib.shop.models import BaykeShopCategory, BaykeShopGoods


class BaykeShopIndexView(TemplateView):
    template_name = 'baykeshop/index.html'

    def get_floors(self):
        """ 获取楼层 """
        category_list = BaykeShopCategory.objects.filter(is_floor=True, parent__isnull=True)
        for category in category_list:
            sub_category_list = category.baykeshopcategory_set.all()
            spu_list = BaykeShopGoods.objects.filter(category__in=sub_category_list)
            category.spu_list = spu_list
        return category_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['floors'] = self.get_floors()
        context['title'] = _('首页')
        return context
        