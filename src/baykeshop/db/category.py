from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseModel


class BaseCategoryModel(BaseModel):
    """
    分类基类
    """
    name = models.CharField(max_length=50, verbose_name=_('名称'))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('父级'))
    is_show = models.BooleanField(default=True, verbose_name=_('是否显示'))
    order = models.IntegerField(default=0, verbose_name=_('排序'))

    class Meta:
        abstract = True
        ordering = ['order']

    @classmethod
    def get_queryset(cls):
        return cls.objects.filter(is_show=True)