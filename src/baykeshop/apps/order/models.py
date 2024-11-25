import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from baykeshop.apps.core.models import BaseModel, BaseCommentModel
from baykeshop.apps.shop.models import BaykeShopSKU

User = get_user_model()


class BaykeShopOrder(BaseModel):
    """订单表"""

    class OrderStatus(models.IntegerChoices):
        WAIT_PAY = 0, _('待支付')
        WAIT_DELIVER = 1, _('待发货')
        WAIT_RECEIVE = 2, _('待收货')
        WAIT_EVALUATE = 3, _('待评价')
        FINISHED = 4, _('已完成')
        CANCEL = 5, _('已取消')
        REFUND = 6, _('已退款')
        WAIT_VERIFY = 7, _('待核销')

    class DeliveryType(models.IntegerChoices):
        SELF_DELIVERY = 0, _('自提')
        EXPRESS = 1, _('快递')
        OTHER = 2, _('其他')
    
    class PayType(models.IntegerChoices):
        ALIPAY = 0, _('支付宝支付')
        WECHAT = 1, _('微信支付')
        OTHER = 2, _('货到付款')

    user = models.ForeignKey(User, verbose_name=_('用户'), on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=50, verbose_name=_('订单号'), editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('订单总价'))
    # 实际的支付金额，由于订单可能部分支付，所以可能与订单总价不相等
    pay_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_('实际支付金额'), 
        blank=True,
        default=0
    )
    receiver = models.CharField(max_length=50, verbose_name=_('收货人'))
    address = models.CharField(max_length=100, verbose_name=_('收货地址'))
    phone = models.CharField(max_length=11, verbose_name=_('联系电话'))
    status = models.SmallIntegerField(choices=OrderStatus.choices, default=0, verbose_name=_('订单状态'))
    delivery_type = models.SmallIntegerField(choices=DeliveryType.choices, default=0, verbose_name=_('配送方式'))
    delivery_id = models.CharField(max_length=50, verbose_name=_('快递单号'), default='', blank=True)
    pay_type = models.SmallIntegerField(choices=PayType.choices, default=0, verbose_name=_('支付方式'))
    pay_id = models.CharField(max_length=50, verbose_name=_('支付流水号'), null=True, blank=True)
    pay_time = models.DateTimeField(verbose_name=_('支付时间'), null=True, blank=True)
    is_refund = models.BooleanField(default=False, verbose_name=_('是否退款'), editable=False)
    is_verify = models.BooleanField(
        default=False, 
        verbose_name=_('是否已核销'), 
        editable=False, 
        help_text=_('核销后，订单状态会自动改为待评价')
    )
    is_delete = models.BooleanField(default=False, verbose_name=_('是否删除'), editable=False)

    class Meta:
        verbose_name = _('订单')
        verbose_name_plural = _('订单')
        ordering = ['-create_time']
        constraints = [
            models.UniqueConstraint(fields=['user', 'order_sn'], name='unique_order_sn')
        ]
    
    def __str__(self):
        return self.order_sn
    
    def get_order_sn(self):
        return '{}{}{}'.format(
            timezone.now().strftime('%Y%m%d%H%M%S'), 
            self.user.id, 
            random.randint(10, 99)
        )
    
    def save(self, *args, **kwargs):
        if not self.order_sn:
            self.order_sn = self.get_order_sn()
        return super().save(*args, **kwargs)
    
    @property
    def payurl(self):
        return reverse('order:order-pay', kwargs={'order_sn': self.order_sn})
    

class BaykeShopOrderItem(BaseModel):
    """订单详情表"""
    order = models.ForeignKey(BaykeShopOrder, verbose_name=_('订单'), on_delete=models.CASCADE)
    sku = models.ForeignKey(BaykeShopSKU, verbose_name=_('商品'), on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('商品价格'))
    quantity = models.PositiveIntegerField(verbose_name=_('购买数量'))
    is_delete = models.BooleanField(default=False, verbose_name=_('是否删除'))

    class Meta:
        verbose_name = _('订单详情')
        verbose_name_plural = _('订单详情')
        ordering = ['-create_time']
        constraints = [
            models.UniqueConstraint(fields=['order', 'sku'], name='unique_order_sku')
        ]
    
    def __str__(self):
        return '{} {}'.format(self.order.order_sn, self.sku.spu.name)
    
    @property
    def total_price(self):
        return self.price * self.quantity
    
    def get_sku_name(self):
        return '{} {}'.format(
            self.sku.spu.name, 
            self.sku.combination.specs.values_list('value', flat=True)
        )
    

class BaykeShopOrderLog(BaseModel):
    """订单日志"""
    order = models.ForeignKey(BaykeShopOrder, verbose_name=_('订单'), on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_('日志内容'))
    user = models.ForeignKey(User, verbose_name=_('操作人'), on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=BaykeShopOrder.OrderStatus.choices, verbose_name=_('日志类型'))

    class Meta:
        verbose_name = _('订单日志')
        verbose_name_plural = _('订单日志')
        ordering = ['-create_time']
    
    def __str__(self):
        return '{} {}'.format(self.order.order_sn, self.type)
    
    @classmethod
    def create_log(cls, order, content, user):
        order_log = BaykeShopOrderLog()
        order_log.order = order
        order_log.user = user
        order_log.content = content
        order_log.type = order.status
        order_log.save()
        return order_log


class BaykeShopOrderComment(BaseCommentModel):
    """订单评价"""
    class CommentSatisfaction(models.IntegerChoices):
        GOOD = 1, _('好评')
        NORMAL = 2, _('中评')
        BAD = 3, _('差评')

    order = models.ForeignKey(
        BaykeShopOrder, 
        verbose_name=_('订单'), 
        on_delete=models.CASCADE
    )
    satisfaction = models.SmallIntegerField(
        choices=CommentSatisfaction.choices, 
        default=CommentSatisfaction.GOOD,
        verbose_name=_('评价满意度')
    )
    score = models.SmallIntegerField(
        default=5, 
        verbose_name=_('评价分数'), 
        help_text=_('1-5分'), 
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        verbose_name = _('订单评价')
        verbose_name_plural = _('订单评价')
        ordering = ['-create_time']
    
    def __str__(self):
        return '{} {}'.format(self.order.order_sn, self.satisfaction)
    
    @classmethod
    def get_spu_comment_queryset(cls, spu):
        orders = BaykeShopOrderItem.objects.filter(sku__spu=spu).values_list('order__id', flat=True)
        queryset = cls.objects.filter(order_id__in=orders)
        return queryset
    
    @classmethod
    def get_spu_comment_count(cls, spu):
        """ 评论总数 """
        return cls.get_spu_comment_queryset(spu).count()
    
    @classmethod
    def get_spu_comment_avg_score(cls, spu):
        """ 获取商品平均评分 """
        return cls.get_spu_comment_queryset(spu).aggregate(models.Avg('score')).get('score__avg') or 4.8

    @classmethod
    def get_spu_comment_rate(cls, spu):
        """ 获取好评率 """
        comments = cls.get_spu_comment_queryset(spu)
        gte_3 = comments.filter(score__gte=3).count()
        rate = gte_3 / comments.count() if comments.count() else 0.98
        return rate * 100