import random
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .base import BaseModel, BaseManager

User = get_user_model()


class BaykeShopOrdersGoodsManager(BaseManager):
    """订单商品管理器"""
    def get_queryset(self):
        return super().get_queryset().select_related('sku').alias(
            total_price=models.ExpressionWrapper(
                models.F('quantity') * models.F('price'),
                output_field=models.DecimalField()
            )
        ).annotate(
            total_price=models.F('total_price')
        )


class BaseOrdersModel(BaseModel):
    """ 订单基类 """

    class ORDER_STATUS(models.IntegerChoices):
        UNPAID = 0, _('未支付')
        # 已支付
        PAID = 1, _('待发货')
        # 已发货
        SHIPPED = 2, _('待收货')
        # 已完成
        FINISHED = 3, _('已完成')
        # 已取消（用户主动删除或后台删除）
        CANCELED = 4, _('已取消')
        # 已过期（长时间未支付）
        EXPIRED = 5, _('已过期')
        # 待核销
        WRITTEN_OFF = 6, _('待核销')
        # 已核销
        WRITTEN_OFFED = 7, _('已核销')
    

    class PayType(models.IntegerChoices):
        ALIPAY = 1, _('支付宝')
        WECHATPAY = 2, _('微信支付')
        CASH = 3, _('货到付款')    
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('用户'))
    order_sn = models.CharField(max_length=50, verbose_name=_('订单号'))
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('总价'))
    status = models.IntegerField(choices=ORDER_STATUS.choices, default=ORDER_STATUS.UNPAID, verbose_name=_('订单状态'))
    pay_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('实际支付金额'))
    # 收货人
    receiver = models.CharField(max_length=50, verbose_name=_('收货人'), blank=True, default='')
    phone = models.CharField(max_length=11, verbose_name=_('手机号码'), blank=True, default='')
    address = models.CharField(max_length=255, verbose_name=_('收货地址'), blank=True, default='')
    pay_type = models.IntegerField(choices=PayType.choices, default=PayType.ALIPAY, verbose_name=_('支付方式'))
    # 支付流水号
    pay_sn = models.CharField(max_length=32, verbose_name=_('支付流水号'), blank=True, default='')
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name=_('支付时间'))
    # 是否核销订单
    is_verify = models.BooleanField(default=False, verbose_name=_('是否核销订单'))
    verify_time = models.DateTimeField(blank=True, null=True, verbose_name=_('核销时间'))
    is_comment = models.BooleanField(default=False, verbose_name=_('是否评价'))

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['user', 'order_sn'], name='unique_order_sn')
        ]

    def get_order_sn(self):
        return '{}{}{}'.format(
            timezone.now().strftime('%Y%m%d%H%M%S'), 
            self.user.id, 
            random.randint(10, 99)
        )

    def save(self, *args, **kwargs):
        if not self.order_sn:
            self.order_sn = self.get_order_sn()
        super().save(*args, **kwargs)


class BaseOrdersGoodsModel(BaseModel):
    """ 订单商品 """
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('价格'))
    quantity = models.IntegerField(default=1, verbose_name=_('数量'))
    specs = models.JSONField(
        verbose_name=_('规格'), 
        default=list,
        help_text=_('规格数据'),
        blank=True
    )
    # 商品SKU数据锁定状态
    sku_sn = models.CharField(max_length=50, verbose_name=_('商品编码'), blank=True, default='')
    name = models.CharField(max_length=50, verbose_name=_('商品名称'), blank=True, default='')
    detail = models.TextField(blank=True, null=True, verbose_name=_('商品详情'))
    image = models.ImageField(upload_to='goods', blank=True, null=True, verbose_name=_('商品主图'))

    objects = BaykeShopOrdersGoodsManager()

    class Meta:
        abstract = True