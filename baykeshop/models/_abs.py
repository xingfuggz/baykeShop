from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from baykeshop.models import tinymce_field


class BaseManager(models.Manager):
    """ 默认管理器 """
    def get_queryset(self):
        return super().get_queryset().filter(is_del=False)


class BaseModelMixin(models.Model):
    """ 模型全局基类 """
    
    add_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False, editable=False)
    
    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class ArticleMixin(BaseModelMixin):
    """ 内容基类视图 """
    title = models.CharField(_("标题"), max_length=100)
    desc = models.CharField(_("描述"), max_length=150, blank=True, default="")
    keywords = models.CharField(_("关键字"), max_length=150, blank=True, default="")
    content = tinymce_field.TinymceField(_("详情"))
    
    class Meta(BaseModelMixin.Meta):
        abstract = True


class GoodsMixin(ArticleMixin):
    """ 商品 """
    after_sale = tinymce_field.TinymceField(_("售后服务"), blank=True, default="")
    
    class Meta:
        abstract = True
        

class ProductMixin(BaseModelMixin):
    """ 规格 """
    pic = models.ImageField(_("主图"), upload_to="pic/%Y/", max_length=200)
    price = models.DecimalField(_("售价"), max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(_("库存"), default=0)
    sales = models.PositiveIntegerField(_("销量"), default=0)
    num = models.CharField(_("商品编号"), max_length=50, blank=True, null=True, unique=True)
    weight = models.PositiveSmallIntegerField(_("重量"), default=0, help_text=_("单位：千克"))
    volume = models.PositiveSmallIntegerField(_("体积"), default=0, help_text=_("单位：立方米"))
    is_release = models.BooleanField(_("上架"), default=True)
    
    class Meta(BaseModelMixin.Meta):
        abstract = True


class OrderMixin(BaseModelMixin):
    
    # TODO

    class Meta:
        abstract = True