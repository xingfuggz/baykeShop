from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baykeshop.contrib.shop'
    verbose_name = _('商品管理')
    verbose_name_plural = _('商品管理')

    def ready(self):
        from . import signals