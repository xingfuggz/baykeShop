from django.contrib import admin

from baykeshop.public.sites import bayke_site
from baykeshop.module.admin.options import BaseModelAdmin
from . import models


@admin.register(models.BaykeArticleCategory, site=bayke_site)
class BaykeArticleCategoryAdmin(BaseModelAdmin):
    '''Admin View for BaykeArticleCategory'''

    list_display = ('name', 'icon', 'desc', 'add_date')
    search_fields = ('name', 'desc')


@admin.register(models.BaykeArticle, site=bayke_site)
class BaykeArticleAdmin(BaseModelAdmin):
    '''Admin View for BaykeArticleCategory'''

    list_display = ('title', 'category', 'add_date')
    search_fields = ('title', 'desc')
    
    def save_model(self, request, obj, form, change) -> None:
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    

bayke_site.register(models.BaykeArticleTag)