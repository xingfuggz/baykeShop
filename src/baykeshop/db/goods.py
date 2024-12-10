from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .fields import RichTextField

User = get_user_model()


class BaseGoodsModel(BaseModel):
    """商品表"""

    class Status(models.IntegerChoices):
        """商品状态"""

        ONLINE = 1, _("上架")
        OFFLINE = 2, _("下架")

    # 商品类型
    class GoodsType(models.IntegerChoices):
        """商品类型"""

        NORMAL = 1, _("普通商品")
        VIRTUAL = 2, _("虚拟商品")

    name = models.CharField(max_length=50, verbose_name=_("商品名称"))
    keywords = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("商品关键字")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("商品描述"))
    # detail = models.TextField(blank=True, null=True, verbose_name=_("商品详情"))
    detail = RichTextField(blank=True, null=True, verbose_name=_("商品详情"))
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.ONLINE, verbose_name=_("商品状态")
    )
    goods_type = models.PositiveSmallIntegerField(
        choices=GoodsType.choices, default=GoodsType.NORMAL, verbose_name=_("商品类型")
    )

    class Meta:
        verbose_name = _("商品")
        verbose_name_plural = _("商品")
        ordering = ["-created_time"]
        abstract = True


class BaseGoodsSKUModel(BaseModel):
    """商品规格"""

    specs = models.JSONField(
        verbose_name=_("规格"), default=list, help_text=_("规格数据"), blank=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("价格"), default=0.00
    )
    sku_sn = models.CharField(
        max_length=50, verbose_name=_("商品编码"), blank=True, default=""
    )
    # 划线价
    line_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("划线价"),
        blank=True,
        default=0.00,
        help_text=_("商品价格划线价，不参与价位计算筛选, 仅供前端显示使用"),
    )
    stock = models.PositiveSmallIntegerField(default=0, verbose_name=_("库存"))
    sales = models.PositiveSmallIntegerField(default=0, verbose_name=_("销量"))

    class Meta:
        verbose_name = _("商品规格")
        verbose_name_plural = _("商品规格")
        ordering = ["-created_time"]
        abstract = True
