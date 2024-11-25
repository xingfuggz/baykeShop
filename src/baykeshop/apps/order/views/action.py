from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ProcessFormView
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse

from baykeshop.apps.order.models import (
    BaykeShopOrder, BaykeShopOrderLog
)
from baykeshop.apps.order.forms import BaykeShopOrderCommentForm

class OrderStatusActionView(LoginRequiredMixin, SingleObjectMixin, ProcessFormView):
    """ 订单状态操作视图 """
    model = BaykeShopOrder
    slug_field = 'order_sn'
    slug_url_kwarg = 'order_sn'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def handle_no_permission(self):
        return JsonResponse({'code': 401, 'msg': '未登录，请登录后操作！'})
    
    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = BaykeShopOrder.OrderStatus.WAIT_EVALUATE
        order.save()
        BaykeShopOrderLog.create_log(
            order, 
            f'{request.user}用户主动执行了确认收货操作', 
            request.user
        )
        return JsonResponse({'code': 200, 'msg': '确认收货成功！'})
    

class CommentActionView(OrderStatusActionView):
    """ 评论操作视图 """
    model = BaykeShopOrder
    slug_field = 'order_sn'
    slug_url_kwarg = 'order_sn'
    context_object_name = 'order'

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        form = BaykeShopOrderCommentForm(request.POST)
        # 判断订单状态
        if order.status != BaykeShopOrder.OrderStatus.WAIT_EVALUATE:
            return JsonResponse({'code': 400, 'errmsg': '订单状态不正确'})
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.order = order
            new_comment.user = request.user
            new_comment.save()
            # 更新订单状态
            order.status = BaykeShopOrder.OrderStatus.FINISHED
            order.save()

            BaykeShopOrderLog.create_log(
                order, 
                f'{request.user}用户评论了订单{order.order_sn}', 
                request.user
            )
            return HttpResponseRedirect(reverse('order:order-list'))
        return JsonResponse({'code': 400, 'msg': '评论失败！', 'data': form.errors})
        
