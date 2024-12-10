from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from django.utils.translation import gettext_lazy as _
from baykeshop.sites import admin as bayke_admin

# Register your models here.
from baykeshop.conf import bayke_settings
from .models import *

admin.site.unregister(Site)

@admin.register(Site)
class BaykeSiteAdmin(SiteAdmin):
    list_display = (
        "domain",
        "name",
    )
    search_fields = ("domain", "name")
    fieldsets = ((None, {"fields": ("domain", "name")}),)

    def has_add_permission(self, request):
        return False


@admin.register(BaykeDictModel)
class BaykeDictModelAdmin(bayke_admin.ModelAdmin):
    list_display = ("key", "name", "created_time")
    search_fields = ("key", "name", "value")
    fieldsets = ((None, {"fields": ("key", "name", "value")}),)

    def get_readonly_fields(self, request, obj=None):
        # 判断是否是系统内置字典
        if hasattr(bayke_settings, obj.key):
            return [
                "key",
            ]
        return super().get_readonly_fields(request, obj)

    def has_delete_permission(self, request, obj=None):
        # 判断是否是系统内置字典
        if obj and hasattr(bayke_settings, obj.key):
            self.message_user(request, _(f"{obj.key}为系统内置字典不允许删除"), "WARNING")
            return False
        return super().has_delete_permission(request, obj)


@admin.register(BaykeBanners)
class BaykeBannersAdmin(bayke_admin.ModelAdmin):
    list_display = ("title", "image", "url", "is_show", "order", "created_time")
    search_fields = ("title", "url")
    fieldsets = ((None, {"fields": ("title", "image", "url", "is_show", "order")}),)
