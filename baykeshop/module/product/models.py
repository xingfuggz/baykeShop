from django.db import models
from baykeshop.models import _abs


class BaykeSpec(_abs.BaseModelMixin):
    """Model definition for BaykeSpec."""
    name = models.CharField(_abs._("规格"), max_length=50)

    # TODO: Define fields here

    class Meta(_abs.BaseModelMixin.Meta):
        verbose_name = _abs._("规格")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BaykeSpecOptions(_abs.BaseModelMixin):
    """ 规格值 """
    spec = models.ForeignKey(BaykeSpec, on_delete=models.CASCADE, verbose_name=_abs._("规格"))
    name = models.CharField(_abs._("规格值"), max_length=50)
    
    class Meta(_abs.BaseModelMixin.Meta):
        verbose_name = _abs._("规格值")
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class BaykeGoods(_abs.GoodsMixin):
    """Model definition for BaykeProduct."""

    # TODO: Define fields here

    class Meta(_abs.BaseModelMixin.Meta):
        verbose_name = _abs._("商品")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class BaykeProduct(_abs.ProductMixin):
    """Model definition for BaykeProduct."""

    goods = models.ForeignKey(BaykeGoods, on_delete=models.CASCADE, verbose_name=_abs._("商品"))
    options = models.ManyToManyField(BaykeSpecOptions, blank=True, verbose_name=_abs._("规格"))
    
    # TODO: Define fields here

    class Meta:
        verbose_name = _abs._("SKU")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.title

