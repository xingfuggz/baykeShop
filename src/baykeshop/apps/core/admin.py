from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.admin import SiteAdmin
# Register your models here.
from baykeshop.site.admin import site as bayke_site
from .models import *

admin.site.unregister(Site)


class ExtendSiteInline(admin.StackedInline):
    model = ExtendSite
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('site', 'logo', 'site_title', 'site_header', 'index_title', 'icp_record' )
        }),
        ('SEO优化', {
            'classes': ('collapse',),
            'fields': ('description', 'keywords')
        }),
    )
    

class ExtendSiteEmailInline(admin.StackedInline):
    model = ExtendSiteEmail
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('site', 'host', 'username', 'password', 'from_email', 'port', 'is_ssl', 'is_tls')
        }),
    )


class ExtendSiteConfigInline(admin.StackedInline):
    model = ExtandSiteConfig
    extra = 1
    readonly_fields = ('site',)
    fieldsets = (
        (None, {
            'fields': ('site', 'key', 'description')
        }),
        ('Value值', {
            'classes': ('collapse',),
            'fields': ('value',)
        }),
    )


@admin.register(Site, site=bayke_site)
class MySiteAdmin(SiteAdmin):
    list_display = ('domain', 'name')
    inlines = [ExtendSiteInline, ExtendSiteEmailInline, ExtendSiteConfigInline]

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False
