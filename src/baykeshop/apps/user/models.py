from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.
from baykeshop.apps.core.models import BaseModel
from baykeshop.apps.core.validators import validate_phone, validate_image_size

User = get_user_model()


class UserProfile(BaseModel):
    """ 用户信息 """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=50, verbose_name=_('昵称'), default='')
    avatar = models.ImageField(
        upload_to='avatar/%Y/%m', 
        default='', 
        verbose_name=_('头像'), 
        validators=[validate_image_size],
        blank=True
    )
    sex = models.CharField(
        max_length=10,
        choices=(('male', '男'), ('female', '女'), ('empty', '未知')), 
        default='male',
        verbose_name=_('性别')
    )
    phone = models.CharField(
        max_length=11, 
        verbose_name=_('手机号'), 
        null=True, 
        blank=True, 
        unique=True,
        validators=[validate_phone]
    )

    class Meta:
        verbose_name = _('用户信息')
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.nickname


class UserAddress(BaseModel):
    """ 用户地址 """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address', verbose_name=_('用户'))
    name = models.CharField(max_length=20, verbose_name=_('收件人'))
    province = models.CharField(max_length=20, verbose_name=_('省份'))
    city = models.CharField(max_length=20, verbose_name=_('城市'))
    district = models.CharField(max_length=20, verbose_name=_('区域'))
    detail_address = models.CharField(max_length=100, verbose_name=_('详细地址'))
    phone = models.CharField(max_length=11, verbose_name=_('手机号'), validators=[validate_phone])
    is_default = models.BooleanField(default=False, verbose_name=_('是否默认'))

    class Meta:
        verbose_name = _('用户地址')
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
    
    def __str__(self):
        return self.name
    
    def get_full_address(self) -> str:
        return '{province}{city}{district}{detail_address}'.format(
            province=self.province,
            city=self.city,
            district=self.district,
            detail_address=self.detail_address
        )

