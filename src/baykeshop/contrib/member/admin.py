from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# Register your models here.

from .models import BaykeShopUser

User = get_user_model()
admin.site.unregister(User)


class BaykeShopUserAdmin(admin.StackedInline):
    model = BaykeShopUser
    extra = 1


@admin.register(User)
class BaseUserAdmin(UserAdmin):
    list_display = ("username", "nickname", "avatar", "email", "mobile", "is_staff")
    list_display_links = ("username", "nickname")
    inlines = (BaykeShopUserAdmin,)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )


    @admin.display(description="头像")
    def avatar(self, obj):
        if not obj.baykeshopuser.avatar:
            return None
        return format_html(
            '<img src="{}" width="40px" height="40px" />', obj.baykeshopuser.avatar.url
        )

    @admin.display(description="昵称")
    def nickname(self, obj):
        return obj.baykeshopuser.nickname

    @admin.display(description="手机")
    def mobile(self, obj):
        return obj.baykeshopuser.mobile
