'''
@file            :models.py
@Description     :全局模型基类
@Date            :2024/11/03 18:23:48
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = get_user_model()


class BaseModel(models.Model):
    """
    自定义的抽象基类模型
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_('更新时间'))
    is_show = models.BooleanField(
        default=True, 
        verbose_name=_('是否显示'), 
        help_text=_('不显示在页面上'), 
        editable=False
    )

    class Meta:
        abstract = True


class BaseUserModel(BaseModel):
    """
    自定义的抽象用户基类模型
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name=_('用户')
    )

    class Meta:
        abstract = True


class BaseCartModel(BaseUserModel):
    """
    自定义的抽象购物车基类模型
    """
    sku = models.ForeignKey(
        'shop.BaykeShopSKU', 
        on_delete=models.CASCADE, 
        verbose_name=_('商品')
    )
    num = models.PositiveBigIntegerField(default=1, verbose_name=_('数量'))
    
    class Meta:
        abstract = True


class BaseOrderModel(BaseUserModel):
    """
    自定义的抽象订单基类模型
    """
    order_sn = models.CharField(max_length=128, verbose_name=_('订单号'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('总价'))
    
    class Meta:
        abstract = True


class BaseOrderSKUModel(BaseModel):
    """
    自定义的抽象订单商品基类模型
    """
    order = models.ForeignKey(
        'shop.BaykeShopOrder', 
        on_delete=models.CASCADE, 
        verbose_name=_('订单')
    )
    sku = models.ForeignKey(
        'shop.BaykeShopSKU', 
        on_delete=models.CASCADE, 
        verbose_name=_('商品')
    )
    num = models.PositiveBigIntegerField(default=1, verbose_name=_('数量'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('单价'))
    
    class Meta:
        abstract = True


class BaseCommentModel(BaseUserModel):
    """
    自定义的抽象评论基类模型
    """
    content = models.TextField(verbose_name=_('评论内容'))
    
    class Meta:
        abstract = True