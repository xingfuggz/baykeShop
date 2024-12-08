from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.
from baykeshop.db import BaseModel, BaseUserModel
from baykeshop.db import validators


User = get_user_model()


class BaykeShopUser(BaseUserModel):
    """用户表"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("用户"))

    def __str__(self):
        return self.user.username


class BaykeShopUserAddress(BaseModel):
    """用户地址"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("用户"))
    name = models.CharField(max_length=50, verbose_name=_("收货人"))
    province = models.CharField(max_length=50, verbose_name=_("省"))
    city = models.CharField(max_length=50, verbose_name=_("市"))
    district = models.CharField(max_length=50, verbose_name=_("区"))
    address = models.CharField(max_length=255, verbose_name=_("详细地址"))
    phone = models.CharField(
        max_length=50, verbose_name=_("手机"), validators=[validators.validate_phone]
    )
    is_default = models.BooleanField(default=False, verbose_name=_("是否默认"))

    class Meta:
        verbose_name = _("用户地址")
        verbose_name_plural = verbose_name
        ordering = ["-created_time"]
        indexes = [
            models.Index(fields=["user", "is_default"], name="user_is_default_idx"),
        ]

    def __str__(self):
        return self.name

    def get_full_address(self):
        return "{province}{city}{district}{address}".format(
            province=self.province,
            city=self.city,
            district=self.district,
            address=self.address,
        )
