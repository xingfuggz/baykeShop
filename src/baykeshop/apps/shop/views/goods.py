from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
# Create your views here.
from baykeshop.apps.core.models import Visit
from ..forms import SearchForm
from ..models import BaykeShopSPU, BaykeShopCategory, BaykeShopBrand
from baykeshop.apps.order.models import BaykeShopOrderComment

class BaykeShopSPUListView(ListView):
    """ 全部商品列表 """
    model = BaykeShopSPU
    template_name = 'shop/list.html'
    paginate_by = 20
    form_class = SearchForm

    def get_queryset(self):
        params = self.request.GET.dict()
        queryset = self.model.get_spu_queryset()
        if params.get('keyword') and self.form_class(data=params).is_valid():
            queryset = queryset.filter(name__icontains=params.get('keyword'))
        return queryset.order_by(self.request.GET.get('sort', '-create_time'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = self.get_category_list().filter(pid__isnull=True)
        context['child_category_list'] = self.get_child_category_list()
        context['is_active'] = self.kwargs.get('pk')
        context['brand_list'] = self.get_brand_list()
        context['brand_id'] = int(self.request.GET.get('brand_id', 0))
        context['sort'] = self.request.GET.get('sort')
        return context
    
    def get_category_list(self):
        return BaykeShopCategory.objects.filter(is_show=True)
    
    def get_child_category_list(self, obj=None):
        """ 获取分类列表 """
        pid_qs = self.get_category_list().filter(pid__isnull=True)
        if obj is None and pid_qs.exists():
            return pid_qs.first().baykeshopcategory_set.filter(is_show=True)
        
        if obj.pid:
            return self.get_category_list().filter(pid=obj.pid)
        return self.get_category_list().filter(pid=obj)
    
    def get_brand_list(self):
        return BaykeShopBrand.objects.filter(is_show=True)


class BaykeShopCategorySPUListView(SingleObjectMixin, BaykeShopSPUListView):
    """ 分类商品列表 """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=BaykeShopCategory.objects.filter(is_show=True))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = BaykeShopSPU.get_spu_queryset().filter(is_show=True, category=self.object)
        # 分类筛选
        if self.object.pid is None:
            category_set = self.object.baykeshopcategory_set.filter(is_show=True)
            queryset = BaykeShopSPU.get_spu_queryset().filter(category__in=category_set)
        # 品牌筛选
        if self.request.GET.get('brand_id'):
            queryset = queryset.filter(brand_id=int(self.request.GET.get('brand_id')))
        return queryset.order_by(self.request.GET.get('sort', '-create_time'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['child_category_list'] = self.get_child_category_list(self.object)
        return context


class BaykeShopSPUDetailView(DetailView):
    """ 商品详情 """
    model = BaykeShopSPU
    template_name = 'shop/detail.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        Visit.objects.create_pv_uv(request, self.get_object())
        return response
    
    def get_queryset(self):
        return self.model.get_spu_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visit'] = self.get_visit_count()
        context['comments'] = self.get_comment_list()
        context['comment_count'] = BaykeShopOrderComment.get_spu_comment_count(self.get_object())
        context['comment_avg_score'] = BaykeShopOrderComment.get_spu_comment_avg_score(self.get_object())
        context['comment_rate'] = BaykeShopOrderComment.get_spu_comment_rate(self.get_object())
        print(context['visit'])
        return context
    
    def get_visit_count(self):
        return Visit.objects.get_uv_pv_count(self.get_object())
    
    def get_comment_list(self):
        queryset = BaykeShopOrderComment.get_spu_comment_queryset(self.get_object())
        paginator = Paginator(queryset, 10)
        page_obj = paginator.get_page(self.request.GET.get('page', 1))
        return page_obj