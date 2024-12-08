from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from baykeshop.db import validators
from .base import BaseModel


User = get_user_model()


class BaseUserModel(BaseModel):
    """用户基础信息"""

    class GenderChoices(models.TextChoices):
        MALE = "male", _("男")
        FEMALE = "female", _("女")
        UNKNOWN = "unknown", _("未知")

    nickname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("昵称")
    )
    avatar = models.ImageField(
        upload_to="avatar", blank=True, null=True, verbose_name=_("头像")
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE,
        verbose_name=_("性别"),
    )
    birthday = models.DateField(blank=True, null=True, verbose_name=_("生日"))
    mobile = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name=_("手机号码"),
        unique=True,
        validators=[validators.validate_phone],
    )
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("QQ"))
    wechat = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("微信")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("简介"))

    class Meta:
        verbose_name = _("用户信息")
        verbose_name_plural = _("用户信息")
        ordering = ["-created_time"]
        abstract = True


class BaseUserAddressModel(BaseModel):
    """用户地址"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("用户"))
    name = models.CharField(max_length=50, verbose_name=_("收货人"))
    province = models.CharField(max_length=50, verbose_name=_("省"))
    city = models.CharField(max_length=50, verbose_name=_("市"))
    district = models.CharField(max_length=50, verbose_name=_("区"))
    address = models.CharField(max_length=255, verbose_name=_("详细地址"))
    phone = models.CharField(max_length=50, verbose_name=_("手机"))
    is_default = models.BooleanField(default=False, verbose_name=_("是否默认"))

    class Meta:
        verbose_name = _("地址")
        verbose_name_plural = verbose_name
        ordering = ["-is_default"]
        abstract = True
