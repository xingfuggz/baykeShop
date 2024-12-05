from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baykeshop.contrib.article'
    verbose_name = _('文章管理')
    verbose_name_plural = _('文章管理')
