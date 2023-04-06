from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

from baykeshop.models import _abs


User = get_user_model()


class BaykeMenu(_abs.CategoryMixin):
    """ 菜单 """
    sort = models.PositiveSmallIntegerField(_abs._("排序"), default=1)

    class Meta:
        ordering = ['-sort']
        verbose_name = _abs._('菜单')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PermMixin(_abs.CategoryMixin):
    """ 权限关系基类 """
    permission = models.OneToOneField(
        Permission, 
        on_delete=models.CASCADE, 
        verbose_name=_abs._("权限"), 
        blank=True, 
        null=True
    )
    menus = models.ForeignKey(
        BaykeMenu, 
        on_delete=models.CASCADE, 
        verbose_name=_abs._("菜单")
    )
    # TODO

    class Meta:
        abstract = True


class BaykePermission(PermMixin):
    """ 权限规则 """
    sort = models.PositiveSmallIntegerField(_abs._("排序"), default=1)
    is_show = models.BooleanField(default=True, verbose_name=_abs._("是否显示"))

    class Meta:
        verbose_name = _abs._('菜单权限')
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.permission.name}"