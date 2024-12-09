from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from baykeshop.db import BaseModel, BaseArticleModel, BaseCategoryModel
# Create your models here.


class BaykeArticleCategory(BaseCategoryModel):
    """ 文章分类 """

    class Meta:
        verbose_name = _('文章分类')
        verbose_name_plural = _('文章分类')
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class BaykeArticleTags(BaseModel):
    """ 文章标签 """
    name = models.CharField(max_length=50, verbose_name=_('标签名称'))

    class Meta:
        verbose_name = _('文章标签')
        verbose_name_plural = _('文章标签')
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class BaykeArticleContent(BaseArticleModel):
    """ 文章内容 """
    category = models.ForeignKey(
        BaykeArticleCategory,
        on_delete=models.SET_NULL, 
        verbose_name=_('文章分类'),
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(
        BaykeArticleTags,
        blank=True,
        verbose_name=_('文章标签')
    )

    class Meta:
        verbose_name = _('文章内容')
        verbose_name_plural = _('文章内容')
        ordering = ['-created_time']

    def __str__(self):
        return self.title
    
    @property
    def description(self):
        desc = strip_tags(self.content)[:250]
        return desc
    
    @property
    def next_article(self):
        """ 下一篇文章 """
        try:
            article = self.get_next_by_created_time()
            return article
        except BaykeArticleContent.DoesNotExist:
            return None
    
    @property
    def prev_article(self):
        """ 上一篇文章 """
        try:
            article = self.get_previous_by_created_time()
            return article
        except BaykeArticleContent.DoesNotExist:
            return None
    

class BaykeSidebar(BaseModel):
    """ 侧边栏 """
    class ModuleChoices(models.TextChoices):
        """ 模板名称 """
        SEARCH = 'search', _('搜索')
        ARCHIVE = 'archive', _('归档')
        NAV = 'nav', _('导航栏')
        TAGS = 'tags', _('标签')
        CUSTOM = 'custom', _('自定义')

    name = models.CharField(max_length=50, verbose_name=_('名称'))
    icon = models.CharField(max_length=50, blank=True, default="mdi mdi-menu", verbose_name=_('图标'))
    module = models.CharField(
        max_length=255, 
        choices=ModuleChoices.choices,
        verbose_name=_('模块'),
        default=ModuleChoices.CUSTOM
    )
    content = models.TextField(
        verbose_name=_('自定义内容'), 
        blank=True, 
        default="", 
        help_text=_('自定义内容，仅在自定义模块下生效，支持html语法')
    )
    is_show = models.BooleanField(default=True, verbose_name=_('是否显示'))
    order = models.IntegerField(default=0, verbose_name=_('排序'))

    class Meta:
        verbose_name = _('侧边栏')
        verbose_name_plural = _('侧边栏')
        ordering = ['order']

    def __str__(self):
        return self.name

    def render(self):
        """ 渲染侧边栏 """
        context = {'sidebar': self}
        return render_to_string(f'baykeshop/sidebar/{self.module}.html', context)
    
    @property
    def navs(self):
        return BaykeArticleCategory.objects.filter(parent__isnull=True)
    
    @property
    def tags(self):
        tags_theme = ['bk-is-primary', 'bk-is-info', 'bk-is-success', 'bk-is-warning', 'bk-is-danger']
        return BaykeArticleTags.objects.annotate(
            count=models.Count('baykearticlecontent'),
            theme=models.Value(tags_theme, output_field=models.JSONField())
        )
    
    @property
    def archive(self):
        return BaykeArticleContent.objects.dates(field_name="created_time", kind="month")[:12]