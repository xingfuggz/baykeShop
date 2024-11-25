from django.template import Library

from baykeshop.apps.shop.models import (
    BaykeShopSPU, BaykeShopSKU, BaykeShopGallery,
    BaykeShopCategory
)
from baykeshop.apps.shop.forms import SearchForm

register = Library()

@register.inclusion_tag('shop/filter.html', takes_context=True)
def filter_template(context):
    """过滤模板"""
    request = context['request']
    context['filter_params'] = request.GET.copy()
    context['filter_params'].pop('page', None)
    context['filter_params'].pop('sort', None)
    context['filter_params'] = context['filter_params'].urlencode()
    return context

@register.simple_tag
def has_specs(obj: BaykeShopSPU):
    """ 判断商品是否为多规格 """
    sku_count = obj.baykeshopsku_set.count()
    if sku_count > 1:
        return True
    return False

@register.inclusion_tag("shop/gallery.html")
def gallery_template(obj: BaykeShopSPU):
    """ 商品相册模板 """
    return {
        'gallerys': obj.baykeshopspugallery_set.all()
    }


def _group_by_spec(data):
    """
    将数据按规格名称分类

    :param data: 包含规格数据的列表
    :return: 按规格名称分类的字典
    """
    grouped_data = {}

    for item in data:
        spec_name = item['combination__specs__spec__name']
        spec_value = item['combination__specs__value']

        if spec_name not in grouped_data:
            grouped_data[spec_name] = []

        grouped_data[spec_name].append(spec_value)
    return grouped_data


@register.inclusion_tag("shop/specs.html")
def specs_template(obj: BaykeShopSPU, request):
    """ 商品规格模板 """
    sku_qs = obj.baykeshopsku_set.all()
    spec_value = sku_qs.values(
        'combination__specs__spec__name',
        'combination__specs__value'
    )

    skus_data = {}
    for sku in sku_qs:
        key = ','.join(sku.combination.specs.order_by('id').values_list('value', flat=True))
        skus_data[key] = {
            'id': sku.id,
            'spu_id': sku.spu.id,
            'price': str(sku.price),
            'stock': sku.stock,
            'num': sku.num,
            'unit': sku.unit,
        }
    return {
        'specs': _group_by_spec(spec_value),
        'skus': skus_data,
        'next_url': request.get_full_path()
    }


@register.inclusion_tag("shop/sku.html")
def sku_template(obj: BaykeShopSKU, request):
    """ 单规格模板 """
    return {
        'sku': obj,
        'sku_data': {
            'id': obj.id,
            'spu_id': obj.spu.id,
            'price': str(obj.price),
            'stock': obj.stock,
            'num': obj.num,
            'unit': obj.unit,
        },
        'next_url': request.get_full_path()
    }


@register.simple_tag
def spu_filter_list(**field_kwargs):
    """ 商品推荐状态 """
    if 'is_show' in field_kwargs:
        del field_kwargs['is_show']
    if 'is_on_sale' in field_kwargs:
        del field_kwargs['is_on_sale']
    return BaykeShopSPU.get_spu_queryset().filter(
        is_show=True, is_on_sale=True, **field_kwargs
    )
    

@register.inclusion_tag("shop/search_form.html")
def search_form(request):
    """ 搜索表单 """
    keyword = request.GET.get('keyword', '')
    form = SearchForm(data={ 'keyword': keyword })
    return {
        'keyword': keyword,
        'form': form,
        'is_valid': form.is_valid()
    }


@register.inclusion_tag("shop/banners.html")
def banners_template():
    """ 轮播图 """
    return {
        'banners': BaykeShopGallery.get_gallery_queryset()
    }

@register.simple_tag
def nav_categorys():
    """ 导航 """
    return BaykeShopCategory.objects.filter(is_nav=True, pid__isnull=True)