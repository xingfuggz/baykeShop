from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your views here.
from baykeshop.apps.shop.models import BaykeShopSKU, BaykeShopCart
from baykeshop.apps.order.models import BaykeShopOrder, BaykeShopOrderLog, BaykeShopOrderItem
from baykeshop.apps.order.forms import BaykeShopOrderCreateForm, BaykeShopOrderCommentForm

class OrderListView(LoginRequiredMixin, ListView):
    """ 订单列表 """
    template_name = 'order/list.html'
    login_url = reverse_lazy('user:login')
    model = BaykeShopOrder
    paginate_by = 2

    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = super().get_queryset().filter(user=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = BaykeShopOrderCommentForm()
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    """ 订单详情 """
    template_name = 'order/detail.html'
    login_url = reverse_lazy('user:login')
    model = BaykeShopOrder
    slug_field = 'order_sn'
    slug_url_kwarg = 'order_sn'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    

class OrderCreateView(LoginRequiredMixin, FormView):
    """ 订单创建 """
    template_name = 'order/create.html'
    login_url = reverse_lazy('user:login')
    form_class = BaykeShopOrderCreateForm
    
    def form_valid(self, form):
        """ 订单创建 """
        cleaned_data = form.cleaned_data
        sku_ids = [int(i) for i in cleaned_data['sku_ids'].split(',') if i]
        skus = BaykeShopSKU.objects.filter(id__in=sku_ids)
        if cleaned_data['source'] == 'detail':
            total_price = skus.first().price * int(cleaned_data['count'])
            # 创建订单
            order = self.create_order(total_price, cleaned_data)
            # 创建订单商品
            for sku in skus:
                self.create_order_item(order, sku, int(cleaned_data['count']))
        elif cleaned_data['source'] == 'cart':
            carts = BaykeShopCart.get_cart_queryset(self.request.user).filter(sku_id__in=sku_ids)
            total_price = sum(carts.values_list('total_price', flat=True))
            # 创建订单
            order = self.create_order(total_price, cleaned_data)
            # 创建订单商品
            for cart in carts:
                self.create_order_item(order, cart.sku, cart.num)
            # 删除购物车数据
            carts.delete()
        return JsonResponse({
            'code': 201, 
            'msg': '订单创建成功,请等待...', 
            'data': {
                'payurl': order.payurl
            }
        })
    
    def form_invalid(self, form):
        """ 订单创建失败 """
        return JsonResponse({
                'code': 400, 'msg': '订单创建失败', 'data': form.errors
            }, json_dumps_params={'ensure_ascii': False}
        )
    
    def create_order(self, total_price, cleaned_data):
        """ 创建订单 """
        order = BaykeShopOrder()
        order.user = self.request.user
        order.total_price = total_price
        order.pay_price = total_price
        order.address = cleaned_data['address']
        order.phone = cleaned_data['phone']
        order.receiver = cleaned_data['receiver']
        order.save()
        # 订单日志
        BaykeShopOrderLog.create_log(
            order, 
            '收银台订单创建',
            self.request.user
        )
        return order
    
    def create_order_item(self, order:BaykeShopOrder, sku:BaykeShopSKU, num:int):
        """ 创建订单商品 """
        order_item = BaykeShopOrderItem()
        order_item.order = order
        order_item.sku = sku
        order_item.price = sku.price
        order_item.quantity = num
        order_item.save()
        return order_item