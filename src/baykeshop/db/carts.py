from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .base import BaseModel


User = get_user_model()


class BaseCartsModel(BaseModel):
    """购物车"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('用户'))
    quantity = models.IntegerField(default=1, verbose_name=_('数量'))

    class Meta:
        abstract = True
    