from django.utils import timezone

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer


from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.conf import bayke_settings
from baykeshop.module.payment.paymethod import AlipayMethod
from baykeshop.module.order.serializer import BaykeOrderInfoSerializer
from baykeshop.module.order.models import BaykeOrderInfo


class AlipayNotifyView(GenericAPIView):
    """ 支付宝回调 """
    serializer_class = BaykeOrderInfoSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = (
        bayke_settings.ALIPAYNOTIFY_TEMPLATE_NAME 
        if bayke_settings.ALIPAYNOTIFY_TEMPLATE_NAME 
        else "baykeshop/payment/alipay_notfiy.html"
    )
    
    def get_queryset(self):
        return BaykeOrderInfo.objects.filter(owner=self.request.user)
    
    def get(self, request, extra_context=None):
        datas = request.query_params.dict()
        signature = datas.pop("sign")
        order_sn = datas.get('out_trade_no')
        trade_no = datas.get('trade_no')
        order = self.get_queryset().filter(order_sn=order_sn)
        success = AlipayMethod(request, order.first()).alipay().verify(datas, signature)
        if success:
            order.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
        context = {
            "order": self.get_serializer(order.first(), many=False).data,
            **(extra_context or {})
        }
        return Response(context)

    def post(self, request, *args, **kwargs):
        datas = request.POST.dict()
        signature = datas.pop("sign")
        order_sn = datas.get('out_trade_no')
        trade_no = datas.get('trade_no')
        order = self.get_queryset().filter(order_sn=order_sn)
        success = AlipayMethod(request, order.first()).alipay().verify(datas, signature)
        if success:
            order.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
        return Response('success')