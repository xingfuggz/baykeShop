from django.db import models

from baykeshop.models import _abs
from baykeshop.module.product.models import BaykeProduct


class BaykeOrderInfo(_abs.OrderMixin):
    """ 订单 """

    class Meta:
        verbose_name = _abs._("订单")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn
    

class BaykeOrderGoods(_abs.BaseModelMixin):
    """ 订单商品兼订单快照 """
    orderinfo = models.ForeignKey(BaykeOrderInfo, on_delete=models.CASCADE, verbose_name=_abs._("订单"))
    title = models.CharField(_abs._("商品标题"), max_length=100, editable=False)
    options = models.JSONField(_abs._("商品规格"), editable=False)
    price = models.DecimalField(_abs._("商品单价"), max_digits=8, decimal_places=2, editable=False)
    content = models.TextField(_abs._("商品详情"), editable=False)
    count = models.IntegerField(default=1, verbose_name=_abs._("数量"))
    product = models.ForeignKey(BaykeProduct, on_delete=models.SET_NULL, blank=True, null=True)
    is_commented = models.BooleanField(default=False, verbose_name="是否已评价")
    
    class Meta:
        verbose_name = _abs._('订单商品')
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.title