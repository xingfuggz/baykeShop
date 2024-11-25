from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
# Create your models here.
from baykeshop.apps.core.models import BaseModel
from baykeshop.apps.core.utils.fields import RichTextField


class BaykeShopCategory(BaseModel):
    """ 商品分类 """
    name = models.CharField(max_length=50, verbose_name=_('分类名称'))
    pid = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('父级分类'))
    icon = models.CharField(max_length=50, verbose_name=_('图标'), blank=True, default='')
    is_floor = models.BooleanField(default=False, verbose_name=_('是否楼层'))
    is_nav = models.BooleanField(default=False, verbose_name=_('是否导航'))
    sort = models.IntegerField(default=0, verbose_name=_('排序'))

    class Meta:
        verbose_name = _('商品分类')
        verbose_name_plural = _('商品分类')
        ordering = ['sort', '-create_time']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:category-spu-list', kwargs={'pk': self.id})
    

class BaykeShopBrand(BaseModel):
    """ 品牌 """
    name = models.CharField(max_length=50, verbose_name=_('品牌名称'))
    description = models.TextField(verbose_name=_('描述'), blank=True, default='')
    logo = models.ImageField(upload_to='brand/%Y/%m/%d', blank=True, null=True, verbose_name=_('品牌logo'))
    sort = models.IntegerField(default=0, verbose_name=_('排序'))
    website = models.URLField(verbose_name=_('官网'), blank=True, default='')

    class Meta:
        verbose_name = _('品牌')
        verbose_name_plural = _('品牌')
        ordering = ['sort', '-create_time']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:spu-list')+f'?brand_id={self.id}'
    

class BaykeShopSPU(BaseModel):
    """ 商品 """
    name = models.CharField(max_length=100, verbose_name=_('商品名称'))
    category = models.ForeignKey(BaykeShopCategory, on_delete=models.CASCADE, verbose_name=_('分类'))
    brand = models.ForeignKey(BaykeShopBrand, on_delete=models.CASCADE, verbose_name=_('品牌'), blank=True, null=True)
    description = models.TextField(verbose_name=_('描述'), blank=True, default='')
    keywords = models.CharField(max_length=100, verbose_name=_('关键字'), blank=True, default='')
    # content = models.TextField(verbose_name=_('商品详情'))
    content = RichTextField(verbose_name=_('商品详情'))
    image = models.ImageField(upload_to='goods/%Y/%m/%d', blank=True, null=True, verbose_name=_('图片'))
    is_boutique = models.BooleanField(default=False, verbose_name=_('精品'))
    is_new = models.BooleanField(default=False, verbose_name=_('新品'))
    is_recommend = models.BooleanField(default=False, verbose_name=_('推荐'))
    is_on_sale = models.BooleanField(default=True, verbose_name=_('是否上架'))
    sort = models.IntegerField(default=0, verbose_name=_('排序'))

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品')
        ordering = ['-create_time']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:spu-detail', kwargs={'pk': self.id})
    
    @classmethod
    def get_spu_queryset(cls):
        return cls.objects.filter(baykeshopsku__isnull=False).alias(
            price=models.Min('baykeshopsku__price'), # 最小价格
            stock=models.Sum('baykeshopsku__stock'), # 库存为sku的库存总数
            num=models.Sum('baykeshopsku__num'),     # 销量为sku的销量总数
        ).annotate(
            price=models.F('price'),
            stock=models.F('stock'),
            num=models.F('num')
        ).order_by('-create_time')

    def has_specs(self, obj):
        """ 判断商品是否为多规格 """
        sku_count = obj.baykeshopsku__specs.count()
        if sku_count > 1:
            return True
        return False
    

class BaykeShopSpec(BaseModel):
    """ 商品规格 """
    name = models.CharField(max_length=50, verbose_name=_('规格类名'))

    class Meta:
        verbose_name = _('商品规格')
        verbose_name_plural = _('商品规格')
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class BaykeShopSpecValue(BaseModel):
    """ 商品规格值 """
    value = models.CharField(max_length=50, verbose_name=_('规格值'))
    spec = models.ForeignKey(BaykeShopSpec, on_delete=models.CASCADE, verbose_name=_('规格'))

    class Meta:
        verbose_name = _('规格值')
        verbose_name_plural = _('规格值')
        ordering = ['-create_time']
        constraints = [
            models.UniqueConstraint(fields=['spec', 'value'], name='unique_spec_value')
        ]
    
    def __str__(self):
        return self.value
    

class BaykeShopSpecValueCombination(BaseModel):
    """ 商品规格组合 """
    specs = models.ManyToManyField(BaykeShopSpecValue, verbose_name=_('规格'))

    class Meta:
        verbose_name = _('规格组合')
        verbose_name_plural = _('规格组合')
        ordering = ['-create_time']

    def __str__(self):
        return ','.join(self.specs.order_by('id').values_list('value', flat=True))


class BaykeShopSKU(BaseModel):
    """ 商品SKU """
    spu = models.ForeignKey(BaykeShopSPU, on_delete=models.CASCADE, verbose_name=_('SPU'))
    combination = models.ForeignKey(
        BaykeShopSpecValueCombination, 
        on_delete=models.SET_NULL, 
        verbose_name=_('规格组合'), 
        blank=True,
        null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('价格'))
    stock = models.PositiveBigIntegerField(default=0, verbose_name=_('库存'))
    num = models.PositiveBigIntegerField(default=0, verbose_name=_('销量'), editable=False)
    sort = models.IntegerField(default=0, verbose_name=_('排序'))
    unit = models.CharField(max_length=50, verbose_name=_('单位'), default='件', blank=True)

    class Meta:
        verbose_name = _('商品SKU')
        verbose_name_plural = _('商品SKU')
        ordering = ['sort', '-create_time']
        constraints = [
            models.UniqueConstraint(fields=['spu', 'combination'], name='unique_spu_combination')
        ]
    
    def __str__(self):
        return self.spu.name


class BaykeShopSPUGallery(BaseModel):
    """ 商品轮播图 """
    spu = models.ForeignKey(BaykeShopSPU, on_delete=models.CASCADE, verbose_name=_('商品'))
    image = models.ImageField(upload_to='goods/%Y/%m/%d', blank=True, null=True, verbose_name=_('图片'))
    sort = models.IntegerField(default=0, verbose_name=_('排序'))

    class Meta:
        verbose_name = _('商品轮播图')
        verbose_name_plural = _('商品轮播图')
        ordering = ['sort', '-create_time']
    
    def __str__(self):
        return f'{self.spu.name} - {self.image}'
    

class BaykeShopGallery(BaseModel):
    """ 轮播图 """
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', verbose_name=_('图片'))
    target = models.CharField(max_length=128, blank=True, verbose_name=_('跳转地址'))
    desc = models.CharField(max_length=128, blank=True, default='', verbose_name=_('描述'))
    sort = models.IntegerField(default=0, verbose_name=_('排序'))
    is_show = models.BooleanField(default=True, verbose_name=_('是否显示'))

    class Meta:
        verbose_name = _('商城轮播图')
        verbose_name_plural = _('商城轮播图')
        ordering = ['sort']

    def __str__(self):
        return self.image.url
    
    @classmethod
    def get_gallery_queryset(cls):
        return cls.objects.filter(is_show=True).order_by('sort')