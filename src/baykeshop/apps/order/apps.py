from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baykeshop.apps.order'
    verbose_name = _('订单管理')

    def ready(self):
        from . import signals
