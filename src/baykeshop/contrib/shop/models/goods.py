from django.db import models
from django.utils.translation import gettext_lazy as _

from baykeshop.db import (
    BaseModel,
    BaseGoodsModel,
    BaseGoodsSKUModel,
    BaseCategoryModel,
    BaseCartsModel,
)
from .managers import (
    BaykeShopGoodsManager,
    BaykeShopCartsManager,
    BaykeShopGoodsSKUManager,
)


class BaykeShopCategory(BaseCategoryModel):
    """商品分类"""

    icon = models.CharField(
        max_length=50, blank=True, default="", verbose_name=_("图标")
    )
    is_floor = models.BooleanField(default=False, verbose_name=_("是否楼层"))
    is_nav = models.BooleanField(default=False, verbose_name=_("是否导航"))

    class Meta:
        verbose_name = _("商品分类")
        verbose_name_plural = _("商品分类")
        ordering = ["order"]

    def __str__(self):
        return self.name


class BaykeShopBrand(BaseModel):
    """商品品牌"""

    name = models.CharField(max_length=50, verbose_name=_("品牌名称"))
    image = models.ImageField(
        upload_to="brand", blank=True, null=True, verbose_name=_("品牌图片")
    )
    order = models.IntegerField(default=0, verbose_name=_("排序"))
    description = models.TextField(blank=True, null=True, verbose_name=_("品牌介绍"))

    class Meta:
        verbose_name = _("商品品牌")
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return self.name


class BaykeShopGoods(BaseGoodsModel):
    """商品"""

    category = models.ManyToManyField(
        BaykeShopCategory, blank=True, verbose_name=_("商品分类")
    )
    brand = models.ForeignKey(
        BaykeShopBrand,
        on_delete=models.SET_NULL,
        verbose_name=_("商品品牌"),
        blank=True,
        null=True,
    )
    # 推荐
    is_recommend = models.BooleanField(default=False, verbose_name=_("商品推荐"))

    objects = BaykeShopGoodsManager()

    class Meta:
        verbose_name = _("商品")
        verbose_name_plural = _("商品")
        ordering = ["-created_time"]

    def __str__(self):
        return self.name

    def has_many_sku(self):
        return self.baykeshopgoodssku_set.count() > 1


class BaykeShopGoodsSKU(BaseGoodsSKUModel):
    """商品SKU"""

    goods = models.ForeignKey(
        BaykeShopGoods, on_delete=models.CASCADE, verbose_name=_("商品")
    )

    objects = BaykeShopGoodsSKUManager()

    class Meta:
        verbose_name = _("商品SKU")
        verbose_name_plural = _("商品SKU")
        ordering = ["-created_time"]

    def __str__(self):
        return self.goods.name


class BaykeShopCarts(BaseCartsModel):
    """购物车"""

    sku = models.ForeignKey(
        BaykeShopGoodsSKU, on_delete=models.CASCADE, verbose_name=_("商品")
    )

    objects = BaykeShopCartsManager()

    class Meta:
        verbose_name = _("购物车")
        verbose_name_plural = _("购物车")
        ordering = ["-created_time"]
        constraints = [
            models.UniqueConstraint(fields=["user", "sku"], name="unique_carts")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.sku.goods.name}"


class BaykeShopSpec(BaseCategoryModel):
    """商品规格"""

    class Meta:
        verbose_name = _("规格模版")
        verbose_name_plural = _("规格模版")
        ordering = ["-created_time"]

    def __str__(self):
        if not self.parent:
            return self.name
        return f"{self.parent.name}:{self.name}"


class BaykeShopGoodsImages(BaseModel):
    """商品图片"""

    goods = models.ForeignKey(
        BaykeShopGoods, on_delete=models.CASCADE, verbose_name=_("商品")
    )
    image = models.ImageField(
        upload_to="goods/images",
        verbose_name=_("商品图片"),
        help_text="_(建议尺寸: 800*800，排在第一个的图片会作为商品主图)",
    )
    order = models.IntegerField(default=0, verbose_name=_("排序"))

    class Meta:
        verbose_name = _("商品图片")
        verbose_name_plural = _("商品图片")
        ordering = ["order"]

    def __str__(self):
        return self.goods.name
