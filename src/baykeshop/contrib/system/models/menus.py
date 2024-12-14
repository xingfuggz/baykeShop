#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件    :menus.py
@说明    :自定义菜单模型
@时间    :2024/12/12 09:37:13
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission

from baykeshop.db import BaseModel


class BaykeMenus(BaseModel):
    """
    自定义菜单
    """

    name = models.CharField(max_length=50, verbose_name=_("菜单名称"))
    icon = models.CharField(
        max_length=50, blank=True, default="", verbose_name=_("菜单图标")
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("父级菜单"),
    )
    permission = models.OneToOneField(
        Permission,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("权限"),
    )
    is_show = models.BooleanField(default=True, verbose_name=_("是否显示"))
    order = models.IntegerField(default=0, verbose_name=_("排序"))

    class Meta:
        verbose_name = _("自定义菜单")
        verbose_name_plural = _("自定义菜单")
        ordering = ["order"]

    def __str__(self):
        return self.name
