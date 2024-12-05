from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from baykeshop.sites import admin as bayke_admin
from .models import BaykeArticleContent, BaykeArticleCategory, BaykeArticleTags, BaykeSidebar


class BaykeArticleCategoryInline(bayke_admin.TabularInline):
    extra = 1
    model = BaykeArticleCategory
    verbose_name = '子分类'
    verbose_name_plural = '子分类'


@admin.register(BaykeArticleCategory)
class BaykeArticleCategoryAdmin(bayke_admin.ModelAdmin):
    """ 文章分类管理器 """
    list_display = ('id', 'name', 'is_show', 'order', 'created_time')
    list_display_links = ('id', 'name')
    list_filter = ('is_show',)
    search_fields = ('name',)
    ordering = ('-order',)
    readonly_fields = ('parent',)
    list_editable = ('is_show', 'order')
    inlines = [BaykeArticleCategoryInline]


@admin.register(BaykeArticleContent)
class BaykeArticleContentAdmin(bayke_admin.ModelAdmin):
    """ 文章内容管理器 """
    list_display = ('id', 'title', 'category', 'user', 'order', 'created_time')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    ordering = ('-created_time',)
    readonly_fields = ('user', )
    filter_horizontal = ('tags',)
    fieldsets = (
        (_('文章信息'), {
            'fields': ('title', 'category', 'tags', )
        }),
        (_('文章内容'), {
            'fields': ('content', 'user', 'order')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['queryset'] = BaykeArticleCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

@admin.register(BaykeArticleTags)
class BaykeArticleTagsAdmin(bayke_admin.ModelAdmin):
    """ 文章标签管理器 """
    list_display = ('id', 'name', 'created_time')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-created_time',)


@admin.register(BaykeSidebar)
class BaykeSidebarAdmin(bayke_admin.ModelAdmin):
    """ 侧边栏管理器 """
    list_display = ('id', 'name', 'icon', 'module', 'order', 'is_show', 'created_time')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-order',)
    list_filter = ('module',)
    list_editable =('order', 'is_show')