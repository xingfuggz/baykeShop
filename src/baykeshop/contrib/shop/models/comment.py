from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from baykeshop.db import BaseModel
from baykeshop.contrib.shop.models import BaykeShopOrders, BaykeShopOrdersGoods

User = get_user_model()

class BaykeShopOrdersComment(BaseModel):
    """
    订单评论
    """

    class ScoreChoices(models.IntegerChoices):
        """
        评分
        """
        ONE = 1, _('⭐')
        TWO = 2, _('⭐⭐')
        THREE = 3, _('⭐⭐⭐')
        FOUR = 4, _('⭐⭐⭐⭐')
        FIVE = 5, _('⭐⭐⭐⭐⭐')

    order = models.ForeignKey(
        BaykeShopOrders,
        verbose_name=_('订单'),
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('用户'),
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        verbose_name=_('评论内容'),
    )
    reply_user = models.ForeignKey(
        User,
        verbose_name=_('回复用户'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reply_comments'
    )
    reply_content = models.TextField(
        verbose_name=_('回复内容'),
        help_text=_('回复内容'),
        null=True,
        blank=True
    )
    status = models.BooleanField(
        verbose_name=_('状态'),
        default=True,
        help_text=_('状态')
    )
    score = models.IntegerField(
        verbose_name=_('评分'),
        choices=ScoreChoices.choices,
        default=ScoreChoices.FIVE
    )   

    class Meta:
        verbose_name = _('订单评论')
        verbose_name_plural = _('订单评论')
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.order.order_sn}'
    
    @classmethod
    def get_spu_queryset(cls, spu):
        orders = BaykeShopOrdersGoods.objects.filter(sku__goods=spu).values_list('orders', flat=True).distinct()
        queryset = cls.objects.filter(order_id__in=orders, status=True)
        return queryset.order_by('-created_time')
    
    @classmethod
    def get_user_queryset(cls, user):
        queryset = cls.objects.filter(user=user)
        return queryset.order_by('-created_time')
    
    def save(self, *args, **kwargs):
        self.user = self.order.user
        return super().save(*args, **kwargs)
    
    def get_reply_user(self):
        if self.reply_user:
            return self.reply_user.username
        return ''
    
    def get_reply_content(self):
        if self.reply_content:
            return self.reply_content
        return ''
    
    # 获取平均分
    @classmethod
    def get_score_avg(cls, spu):
        score_avg = cls.get_spu_queryset(spu).aggregate(
            score_avg=models.Avg('score')
        ).get('score_avg') or 4.8
        return round(score_avg, 1)
    
    # 获取评论总数
    @classmethod
    def get_comment_count(cls, spu):
        return cls.get_spu_queryset(spu).count()
    
    # 获取好评率
    @classmethod
    def get_spu_comment_avg_score(cls, spu):
        """ 获取商品好评率  """
        gte_3 = cls.get_spu_queryset(spu).filter(score__gte=3).count()
        rate = gte_3 / cls.get_comment_count(spu) if cls.get_comment_count(spu) else 0.98
        return round(rate * 100, 1)
    
    @classmethod
    def get_user_comment_avg_score(cls, user):
        """ 获取用户好评率 """
        gte_3 = cls.get_user_queryset(user).filter(score__gte=3).count()
        rate = gte_3 / cls.get_user_queryset(user).count() if cls.get_user_queryset(user).count() else 0.98
        return round(rate * 100, 2)