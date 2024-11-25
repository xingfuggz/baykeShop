from django.contrib import admin

# Register your models here.
from baykeshop.site.admin import site as bayke_site
from .models import (
    BaykeArticle, BaykeArticleCategory, BaykeArticleTags
)


@admin.register(BaykeArticle, site=bayke_site)
class BaykeArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'is_show', 'is_top', 'is_original', 'is_recommend', 'create_time', 'update_time')
    list_filter = ('is_show', 'is_top', 'is_original', 'is_recommend',)
    list_display_links = ('id', 'title')
    search_fields= ('title', 'desc')
    readonly_fields = ('author', )
    filter_horizontal = ('tags',)
    
    def save(self, *args, **kwargs):
        self.author = self.request.user
        super().save(*args, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaykeArticleCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BaykeArticleTags, site=bayke_site)
class BaykeArticleTagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time')
    search_fields = ('name',)


class BaykeArticleCategoryInline(admin.StackedInline):
    extra = 1
    model = BaykeArticleCategory
    verbose_name = '子分类'
    verbose_name_plural = '子分类'


@admin.register(BaykeArticleCategory, site=bayke_site)
class BaykeArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'is_show', 'sort', 'create_time')
    list_filter = ('is_show',)
    search_fields = ('name',)
    list_editable = ('is_show', 'sort')
    list_display_links = ('id', 'name')
    readonly_fields = ('parent',)
    inlines = [BaykeArticleCategoryInline]