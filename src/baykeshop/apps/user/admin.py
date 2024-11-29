from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.html import format_html
# Register your models here.
from baykeshop.site.admin import site as bayke_site
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = _('扩展信息')
    verbose_name_plural = _('扩展信息')


@admin.register(User, site=bayke_site)
class BaykeUserAdmin(UserAdmin):
    list_display = ('username', 'avatar', 'email', 'is_staff', 'date_joined', 'last_login')
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
    inlines = (UserProfileInline,)

    @admin.display(description=_('头像'))
    def avatar(self, obj):
        if obj.profile.avatar:
            return format_html('<img src="{}" width="40px" height="40px" />', obj.profile.avatar.url)
        else: 
            return ''
        

@admin.register(Group, site=bayke_site)
class BaykeGroupAdmin(GroupAdmin):
    pass
