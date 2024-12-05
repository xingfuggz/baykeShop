from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from baykeshop.contrib.shop.models import BaykeShopOrders
from baykeshop.contrib.member.forms import BaykeShopOrdersCommentForm


class BaykeShopOrdersListView(LoginRequiredMixin, ListView):
    """ 订单列表 """
    template_name = 'baykeshop/member/order_list.html'
    login_url = reverse_lazy('member:login')
    model = BaykeShopOrders
    paginate_by = 10
    ordering = '-created_time'

    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = super().get_queryset().filter(user=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('我的订单')
        context['comment_form'] = BaykeShopOrdersCommentForm()
        return context
    

class BaykeShopOrdersDetailView(LoginRequiredMixin, DetailView):
    """ 订单详情 """
    template_name = 'baykeshop/member/order_detail.html'
    login_url = reverse_lazy('member:login')
    model = BaykeShopOrders
    slug_field = 'order_sn'
    slug_url_kwarg = 'order_sn'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('订单详情')
        return context
    