from django.contrib.admin.apps import AdminConfig


class ExtendSiteAdminConfig(AdminConfig):
    default_site = 'baykeshop.site.admin.AdminSite'