from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from baykeshop.apps.core.models import BaseModel
from .goods import BaykeShopSKU

User = get_user_model()


class BaykeShopCart(BaseModel):
    """购物车"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('用户'))
    sku = models.ForeignKey(BaykeShopSKU, on_delete=models.CASCADE, verbose_name=_('商品'))
    num = models.PositiveIntegerField(default=1, verbose_name=_('数量'))

    class Meta:
        verbose_name = _('购物车')
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
        constraints = [ 
            models.UniqueConstraint(fields=['user', 'sku'], name='unique_cart') 
        ]

    def __str__(self):
        return f'{self.user.username}的购物车'
    
    @classmethod
    def get_cart_queryset(cls, user):
        """获取购物车商品列表"""
        return cls.objects.filter(is_show=True, user=user).alias(
            total_price=models.ExpressionWrapper(
                models.F('sku__price') * models.F('num'), 
                output_field=models.DecimalField()
            )
        ).annotate(
            total_price=models.F('total_price'),
        )
    
    @classmethod
    def get_cart_count(cls, user):
        """获取购物车数量"""
        return cls.get_cart_queryset(user).count()
    
    @classmethod
    def get_cart_total_price(cls, user):
        """获取购物车总金额"""
        return sum(cls.get_cart_queryset(user).values_list('total_price', flat=True))
    
    @classmethod
    def get_cart_total_num(cls, user):
        """获取购物车总数量"""
        return sum(cls.get_cart_queryset(user).values_list('num', flat=True))
    
    @classmethod
    def get_cart_total_price_and_num(cls, user):
        """获取购物车总金额和总数量"""
        return cls.get_cart_total_price(user), cls.get_cart_total_num(user)
    
    @classmethod
    def _is_valid(cls, request, sku_id:int):
        """校验购物车商品是否合法"""
        is_valid = True
        user = request.user
        sku_qs = BaykeShopSKU.objects.filter(id=sku_id)
        # 未登录或sku不存在
        if not user.is_authenticated or not sku_qs.exists():
            is_valid = False
        return is_valid, user, sku_qs.first()
    
    @classmethod
    def add_cart(cls, request, sku_id:int, num:int):
        """添加购物车"""
        is_valid, user, sku = cls._is_valid(request, sku_id)
        if not is_valid: return False
        cart_qs = cls.objects.filter(user=user, sku=sku)
        if cart_qs.exists():
            cart_qs.update(num=models.F('num') + num)
        else:
            cls.objects.create(user=user, sku=sku, num=num)
        return True
    
    @classmethod
    def del_cart(cls, request, sku_id:int):
        """删除购物车"""
        is_valid, user, sku = cls._is_valid(request, sku_id)
        if not is_valid: return False
        cls.objects.filter(user=user, sku=sku).delete()
        return True
    
    @classmethod
    def change_num(cls, request, sku_id:int, num:int):
        """修改购物车数量"""
        is_valid, user, sku = cls._is_valid(request, sku_id)
        if not is_valid: return False
        cls.objects.filter(user=user, sku=sku).update(num=num)
        return True