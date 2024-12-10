from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator

from baykeshop.contrib.system.models import Visit
from baykeshop.contrib.shop.models import (
    BaykeShopCategory, BaykeShopGoods,
    BaykeShopOrdersComment
)


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

    def get(self, request, *args, **kwargs):
        Visit.objects.create_pv_uv(request, self.get_object())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().name
        context['images'] = self.get_images()
        context['recommends'] = self.get_recommend_queryset()
        context['comments'] = self.get_comments()
        context['score_avg'] = self.get_score_avg()
        context['like_score'] = self.get_like_score()
        context['comments_count'] = self.get_comments_count()
        return context
    
    def get_images(self):
        """ 获取商品图片 """
        queryset = self.get_object().baykeshopgoodsimages_set.order_by('order')
        return queryset
    
    def get_recommend_queryset(self):
        """ 获取同类别推荐的商品，按销量排序，排除当前商品 """
        cates = self.get_object().category.all()
        queryset = BaykeShopGoods.objects.filter(
            is_recommend=True, 
            category__in=cates
        ).exclude(
            id=self.get_object().id
        ).order_by('-sales')
        return queryset[:5]

    def get_comments(self):
        queryset = BaykeShopOrdersComment.get_spu_queryset(self.get_object())
        paginator = Paginator(queryset, 20)
        page_obj = paginator.get_page(self.request.GET.get('page', 1))
        return page_obj
    
    def get_score_avg(self):
        """ 获取商品平均评分 """
        return BaykeShopOrdersComment.get_score_avg(self.get_object())
    
    def get_like_score(self):
        """ 好评率 """
        return BaykeShopOrdersComment.get_spu_comment_avg_score(self.get_object())
    
    def get_comments_count(self):
        """ 获取商品评论数 """
        return BaykeShopOrdersComment.get_comment_count(self.get_object())



class BaykeShopSearchView(BaykeShopGoodsListView):
    """商品搜索"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "商品搜索"
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset =queryset.filter(name__icontains=keyword)
            return self.filter_queryset(queryset)
        return queryset