from django.db import models

from baykeshop.models import _abs


class BaykeArticleTag(_abs.BaseModelMixin):
    
    name = models.CharField(_abs._("标签名"), max_length=50)
    
    class Meta:
        verbose_name = _abs._("文章标签")
        verbose_name_plural = verbose_name
        ordering = ['-add_date']
        
    def __str__(self) -> str:
        return self.name


class BaykeArticleCategory(_abs.CategoryMixin):
    
    class Meta:
        verbose_name = _abs._("文章分类")
        verbose_name_plural = verbose_name
        ordering = ['-add_date']
        
    def __str__(self) -> str:
        return self.name
        

class BaykeArticle(_abs.ArticleMixin):
    
    category = models.ForeignKey(BaykeArticleCategory, on_delete=models.CASCADE, verbose_name=_abs._("分类"))
    tags = models.ManyToManyField(BaykeArticleTag, blank=True, verbose_name=_abs._("标签"))
    
    class Meta:
        verbose_name = _abs._("文章")
        verbose_name_plural = verbose_name
        ordering = ['-add_date']
        
    def __str__(self) -> str:
        return self.title