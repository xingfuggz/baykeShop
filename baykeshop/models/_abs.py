from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.contrib.sites.managers import CurrentSiteManager

from baykeshop.models import tinymce_field


User = get_user_model()


class BaseManager(models.Manager):
    """ 默认管理器 """
    def get_queryset(self):
        return super().get_queryset().filter(is_del=False)


class BaseModelMixin(models.Model):
    """ 模型全局基类 """
    
    add_date = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(auto_now=True)
    site = models.ForeignKey(
        Site, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        help_text=_("关联站点，如果选择，该信息仅在指定站点显示")
    )
    is_del = models.BooleanField(default=False, editable=False)
    
    objects = BaseManager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class ImageMixin(BaseModelMixin):
    """ 图片基类 """
    img = models.ImageField(_("图片"), upload_to="upload/", max_length=200)
    desc = models.CharField(_("图片说明"), max_length=150, blank=True, default="")
    # TODO

    class Meta(BaseModelMixin.Meta):
        abstract = True


class CategoryMixin(BaseModelMixin):
    """ 分类模型基类 """
    name = models.CharField(_("分类名称"), max_length=50)
    icon = models.CharField(_("分类图标"), max_length=50, blank=True, default="")
    desc = models.CharField(_("描述"), max_length=150, blank=True, default="")
    keywords = models.CharField(_("关键字"), max_length=150, blank=True, default="")
    
    class Meta(BaseModelMixin.Meta):
        abstract = True


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
    pic = models.ImageField(_("主图"), upload_to="pic/%Y/", max_length=200)
    freight = models.DecimalField(_("运费"), max_digits=5, decimal_places=2, blank=True, default=0.00)
    
    class Meta:
        abstract = True
        

class ProductMixin(BaseModelMixin):
    """ 规格 """
    pic = models.ImageField(_("主图"), upload_to="pic/%Y/", max_length=200)
    price = models.DecimalField(_("售价"), max_digits=8, decimal_places=2)
    cost_price = models.DecimalField(_("原价"), max_digits=10, decimal_places=2, blank=True, default=0)
    stock = models.PositiveIntegerField(_("库存"), default=0)
    sales = models.PositiveIntegerField(_("销量"), default=0, editable=False)
    num = models.CharField(_("商品编号"), max_length=50, blank=True, null=True, unique=True)
    weight = models.PositiveSmallIntegerField(_("重量"), default=0, help_text=_("单位：千克"))
    volume = models.PositiveSmallIntegerField(_("体积"), default=0, help_text=_("单位：立方米"))
    is_release = models.BooleanField(_("上架"), default=True)
    
    class Meta(BaseModelMixin.Meta):
        abstract = True


class OrderMixin(BaseModelMixin):
    """ 订单模型基类 """
    class PayMethodChoices(models.IntegerChoices):
        CASH = 1, _('货到付款')
        ALIPAY = 2, _('支付宝')
        WECHATPAY = 3, _('微信支付')
        OVERPAY = 4, _('余额支付')

    class OrderStatusChoices(models.IntegerChoices):
        TOBPAY = 1, _('待支付')
        TOBDELIVER = 2, _('待发货')
        TOBRECEIVED = 3, _('待收货')
        TOBEVALUATE = 4, _('待评价')
        COMPLETE = 5, _('已完成')
        CANCELLED = 6, _('已取消')
    
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="用户",
        editable=False
    )
    order_sn = models.CharField(
        blank=True,
        default="",
        unique=True,
        max_length=32,
        editable=False,
        verbose_name="订单号",
        help_text="订单号"
    )
    trade_sn = models.CharField(
        blank=True, null=True,
        unique=True, max_length=64,
        verbose_name="交易号",
        help_text="交易号",
        editable=False
    )
    pay_status = models.IntegerField(
        choices=OrderStatusChoices.choices,
        default=1,
        verbose_name="支付状态",
        help_text="支付状态"
    )
    pay_method = models.IntegerField(
        choices=PayMethodChoices.choices,
        verbose_name="支付方式",
        help_text="支付方式",
        blank=True,
        null=True,
        editable=False
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="商品总金额"
    )
    order_mark = models.CharField(
        blank=True,
        default="",
        max_length=100,
        verbose_name="订单备注",
        help_text="订单备注"
    )
    name = models.CharField("签收人", max_length=50, default="")
    phone = models.CharField("手机号", max_length=11, default="")
    email = models.EmailField("邮箱", blank=True, default="", max_length=50)
    address = models.CharField("地址", max_length=200)
    pay_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="支付时间",
        help_text="支付时间",
        editable=False
    )
    # TODO

    class Meta(BaseModelMixin.Meta):
        abstract = True
        
    def __str__(self):
        return self.order_sn

    @classmethod
    def get_pay_method(cls):
        # 支付方式列表字典
        return dict(cls.PayMethodChoices.choices)

    @classmethod
    def get_pay_default(cls):
        # 获取支付方式的默认值
        return cls._meta.get_field('pay_method').default