from django.db import models
from django.urls import reverse

from baykeshop.models import _abs


class BaykeCategory(_abs.CategoryMixin):
    """Model definition for BaykeCategory."""
    
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    pic = models.ImageField(_abs._("封面图"), upload_to="product/category/", max_length=200)
    is_nav = models.BooleanField(default=False, verbose_name=_abs._("是否导航"))

    # TODO: Define fields here

    class Meta(_abs.BaseModelMixin.Meta):
        verbose_name = _abs._("分类")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
    @classmethod
    def get_cates(cls):
        cates = cls.objects.filter(is_nav=True, parent__isnull=True)
        for cate in cates:
            cate.sub_cates = cate.baykecategory_set.filter(is_nav=True)
        return cates
    
    def get_absolute_url(self):
        return reverse('baykeshop:cate_detail', kwargs={'pk': self.pk})


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
    
    categorys = models.ManyToManyField(BaykeCategory, blank=True, verbose_name=_abs._("分类"))
    
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
        verbose_name = _abs._("商品规格")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.title

