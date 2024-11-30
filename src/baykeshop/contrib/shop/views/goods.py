from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin, DetailView

from baykeshop.contrib.shop.models import BaykeShopCategory, BaykeShopGoods


class BaykeShopGoodsListView(ListView):
    """商品列表"""
    template_name = 'baykeshop/shop/list.html'
    paginate_by = 20
    model = BaykeShopGoods
    ordering = ('-created_time',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "商品列表"
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)

    def filter_queryset(self, queryset):
        brand_id = self.request.GET.get("brand_id")
        sort = self.request.GET.get("sort", "-created_time")
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if sort:
            queryset = queryset.order_by(sort)
        return queryset


class BaykeShopCategoryListView(SingleObjectMixin, BaykeShopGoodsListView):
    """商品分类列表"""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=BaykeShopCategory.objects.all())
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        # 顶级分类返回所有子分类的商品
        queryset = BaykeShopGoods.objects.filter(category__id=self.object.id)
        if self.object.parent is None:
            baykeshopcategory_set = self.object.baykeshopcategory_set.all()
            queryset = BaykeShopGoods.objects.filter(category__in=baykeshopcategory_set)
            return self.filter_queryset(queryset)
        return self.filter_queryset(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context
    

class BaykeShopGoodsDetailView(DetailView):
    """商品详情"""
    model = BaykeShopGoods
    template_name = 'baykeshop/shop/detail.html'
    context_object_name = 'spu'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().name
        context['images'] = self.get_images()
        context['recommends'] = self.get_recommend()
        return context
    
    def get_images(self):
        queryset = self.get_object().baykeshopgoodsimages_set.order_by('order')
        return queryset
    
    def get_recommend(self):
        cates = self.get_object().category.all()
        # 获取同类别推荐的商品，按销量排序，排除当前商品
        queryset = BaykeShopGoods.objects.filter(
            is_recommend=True, 
            category__in=cates
        ).exclude(
            id=self.get_object().id
        ).order_by('-sales')
        return queryset[:5]