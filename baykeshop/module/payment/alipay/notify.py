from django.views.generic import View
from django.template.response import TemplateResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from baykeshop.config.settings import bayke_settings
from baykeshop.module.payment.alipay.pay import alipay
from baykeshop.public.mixins import LoginRequiredMixin
from baykeshop.models import BaykeShopOrderInfo


class AlipayNotifyView(LoginRequiredMixin, View):
    
    template_name = bayke_settings.ALIPAYNOTIFY_TEMPLATE_NAME
    
    def get(self, request, extra_context=None):
        datas = request.GET.dict()
        signature = datas.pop("sign")
        success = alipay.verify(datas, signature)
        if success:
            order_sn = datas.get('out_trade_no')
            trade_no = datas.get('trade_no')
            # trade_status = datas.get('trade_status')
            order = BaykeShopOrderInfo.objects.filter(order_sn=order_sn)
            order.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
        context = {
            "order": order.first(),
            **(extra_context or {})
        }
        return TemplateResponse(request, [self.template_name or "baykeshop/payment/alipay_notify.html"], context)
        
    def post(self, request, *args, **kwargs):
        datas = request.POST.dict()
        signature = datas.pop("sign")
        success = alipay.verify(datas, signature)
        if success:
            order_sn = datas.get('out_trade_no')
            trade_no = datas.get('trade_no')
            # trade_status = datas.get('trade_status')
            order = BaykeShopOrderInfo.objects.filter(order_sn=order_sn)
            order.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
        return HttpResponse('success')