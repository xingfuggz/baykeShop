from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .fields import RichTextField

User = get_user_model()


class BaseArticleModel(BaseModel):
    """文章基类模型"""

    title = models.CharField(max_length=50, verbose_name=_("标题"))
    content = RichTextField(verbose_name=_("内容"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("作者"), blank=True, null=True
    )
    image = models.ImageField(
        upload_to="article", blank=True, null=True, verbose_name=_("图片")
    )
    order = models.IntegerField(default=0, verbose_name=_("排序"))

    class Meta:
        ordering = ["-order", "-created_time"]
        abstract = True
