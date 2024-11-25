from django.views.generic import TemplateView
from baykeshop.apps.shop.models import BaykeShopCategory, BaykeShopSPU


class BaykeShopIndexView(TemplateView):
    template_name = 'shop/index.html'

    def get_floors(self):
        """ 获取楼层 """
        category_list = BaykeShopCategory.objects.filter(is_floor=True, pid__isnull=True)
        for category in category_list:
            sub_category_list = category.baykeshopcategory_set.all()
            spu_list = BaykeShopSPU.get_spu_queryset().filter(category__in=sub_category_list)
            category.spu_list = spu_list
        return category_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['floors'] = self.get_floors()
        return context
        