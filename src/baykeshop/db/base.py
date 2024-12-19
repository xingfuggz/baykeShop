from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import gettext_lazy as _
from .manager import BaseManager

User = get_user_model()


class BaseModel(models.Model):
    """
    基础模型
    """
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name=_("站点"),
        editable=False,
        blank=True,
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("创建时间"))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_("更新时间"))
    is_delete = models.BooleanField(
        default=False, editable=False, verbose_name=_("是否删除")
    )

    objects = BaseManager()
    current_site = CurrentSiteManager()

    class Meta:
        abstract = True
        ordering = ["-created_time"]

    def save(self, *args, **kwargs):
        self.site = Site.objects.get_current()
        super().save(*args, **kwargs)
