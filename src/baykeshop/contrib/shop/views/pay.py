from django.views.generic import DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.decorators import method_decorator

from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from baykeshop.contrib.shop.models.orders import BaykeShopOrders
from baykeshop.contrib.system.models import BaykeDictModel


class BaykeShopOrdersPayView(LoginRequiredMixin, DetailView):
    context_object_name = "order"
    login_url = reverse_lazy("member:login")
    model = BaykeShopOrders
    slug_field = "order_sn"
    slug_url_kwarg = "order_sn"
    template_name = "baykeshop/shop/pay.html"

    def get_queryset(self):
        return BaykeShopOrders.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("订单支付")
        return context


class AlipayCallBackVerifySignMixin:
    """支付宝支付回调，验签"""

    def has_verify_sign(self, data):
        """验签
        data是从请求中获得的字典数据，携带 sign和sign_type
        """
        sign = data.pop("sign")
        sign_type = data.pop("sign_type")
        alipay_public_key = BaykeDictModel.get_key_value("ALIPAY_PUBLIC_KEY")
        # 去除sign和sign_type参数之后进行升序排列，拼装请求参数用支付宝公钥进行验签
        message = "&".join(
            [
                f"{k}={v}"
                for k, v in dict(
                    sorted(data.items(), key=lambda d: d[0], reverse=False)
                ).items()
            ]
        )
        flag = verify_with_rsa(
            alipay_public_key, message.encode("UTF-8", "strict"), sign
        )
        return flag


@method_decorator(csrf_exempt, name="dispatch")
class AlipayCallbackView(AlipayCallBackVerifySignMixin, View):
    """支付宝支付结果通知"""

    def get(self, request, *args, **kwargs):
        """支付宝同步通知"""
        data = request.GET.dict()
        success = self.has_verify_sign(data)
        order_sn = data.get("out_trade_no")
        if success:
            order = BaykeShopOrders.objects.filter(order_sn=order_sn).first()
            if order:
                order.pay_time = timezone.now()
                order.pay_sn = data.get("trade_no")
                order.status = BaykeShopOrders.OrderStatus.PAID
                order.save()
            return HttpResponseRedirect(
                reverse("member:orders-detail", kwargs={"order_sn": order_sn})
            )
        return HttpResponse("success")

    def post(self, request, *args, **kwargs):
        """支付宝异步通知"""
        data = request.POST.dict()
        order_sn = data.get("out_trade_no")
        success = self.has_verify_sign(data)
        if success:
            order = BaykeShopOrders.objects.filter(order_sn=order_sn).first()
            if order:
                order.pay_time = timezone.now()
                order.pay_sn = data.get("trade_no")
                order.status = BaykeShopOrders.OrderStatus.PAID
                order.save()
            return HttpResponse("success")
        