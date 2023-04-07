from django.db import models

from baykeshop.models import _abs


class BaykeBanner(_abs.ImageMixin):
    """Model definition for BaykeBanner."""
    place = models.CharField(
        _abs._("位置标识"), 
        max_length=50, 
        blank=True, 
        null=True, 
        unique=True, 
        help_text=_abs._("留空则为首页banner，否则为指定位置banner")
    )
    target_url = models.CharField(_abs._("跳转地址"), max_length=150, blank=True, default="")
    sort = models.PositiveSmallIntegerField(_abs._("排序"), default=1)
    # TODO: Define fields here

    class Meta(_abs.BaseModelMixin.Meta):
        verbose_name = _abs._("轮播图")
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return f"{self.place}【{self.img.url}】" if self.place else f"Home Banner{self.img.url}"
