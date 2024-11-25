from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.
from baykeshop.apps.core.models import BaseModel
from baykeshop.apps.core.utils.fields import RichTextField

User = get_user_model()

class BaykeArticleCategory(BaseModel):
    """文章分类"""
    name = models.CharField(max_length=50, verbose_name=_('分类名称'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('父级分类'))
    description = models.TextField(verbose_name=_('描述'), blank=True, default='')
    is_show = models.BooleanField(default=True, verbose_name=_('是否显示'))
    sort = models.IntegerField(default=0, verbose_name=_('排序'))

    class Meta:
        verbose_name = _('文章分类')
        verbose_name_plural = verbose_name
        ordering = ['sort']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('article:article_category', kwargs={'pk': self.id})
    

class BaykeArticle(BaseModel):
    """文章"""
    title = models.CharField(max_length=100, verbose_name=_('标题'))
    desc = models.CharField(
        verbose_name=_('描述'), 
        blank=True, 
        default='',
        max_length=150,
        help_text=_('文章描述，用于SEO优化')
    )
    # content = models.TextField(verbose_name=_('内容'))
    content = RichTextField(verbose_name=_('内容'))
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name=_('作者'), 
        editable=False,
        blank=True,
        null=True
    )
    category = models.ForeignKey(BaykeArticleCategory, on_delete=models.CASCADE, verbose_name=_('分类'))
    image = models.ImageField(upload_to='article/%Y/%m/%d', blank=True, null=True, verbose_name=_('图片'))
    is_top = models.BooleanField(default=False, verbose_name=_('置顶'))
    is_recommend = models.BooleanField(default=False, verbose_name=_('推荐'))
    is_original = models.BooleanField(default=False, verbose_name=_('原创'))
    tags = models.ManyToManyField('BaykeArticleTags', verbose_name=_('标签'), blank=True)
    is_show = models.BooleanField(default=True, verbose_name=_('是否显示'))
    sort = models.IntegerField(default=0, verbose_name=_('排序'))

    class Meta:
        verbose_name = _('文章')
        verbose_name_plural = verbose_name
        ordering = ['sort']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article:article_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        from django.utils.html import strip_tags
        self.desc = self.desc if self.desc else strip_tags(self.content[:150])
        super().save(*args, **kwargs)


class BaykeArticleTags(BaseModel):
    """文章标签"""
    name = models.CharField(max_length=50, verbose_name=_('标签名称'))

    class Meta:
        verbose_name = _('文章标签')
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('article:article_tag', kwargs={'pk': self.pk})