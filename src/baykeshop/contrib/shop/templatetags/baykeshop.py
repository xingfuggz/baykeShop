import json

from django.template import Library
from baykeshop.contrib.shop.models import (
    BaykeShopCategory, BaykeShopBrand, BaykeShopGoods
)

register = Library()

@register.simple_tag
def paginator_range(page_obj, on_each_side=1):
    """ 分页页码数据 """
    return page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=on_each_side)


@register.inclusion_tag("baykeshop/tags/pagination.html")
def paginator_template(page_obj, request):
    """分页导模版 """
    params = request.GET.copy()
    params.pop("page", None)
    return {
        "urlencode": params.urlencode(),
        "page_obj": page_obj
    }


@register.inclusion_tag("baykeshop/tags/filters.html", takes_context=True)
def filters_template(context, request):
    """过滤器模板"""
    params = request.GET.copy()
    params.pop("page", None)
    params.pop("sort", None)
    params = params.urlencode()
    kwargs = context['view'].kwargs
    return {
        "request": request,
        "filter_params": params,
        "category_id": kwargs.get("pk", None),
        "object": context.get("object"),
        "brand_id": int(request.GET.get("brand_id", 0))
    }

def __parent_category():
    return BaykeShopCategory.objects.filter(parent__isnull=True)

def __child_category(cate_id=None):
    try:
        cate = BaykeShopCategory.objects.get(id=cate_id)
        # 如果是子类
        if cate.parent:
            # 获取同类
            queryset = cate.parent.baykeshopcategory_set.all()
        else:
            # 获取子类
            queryset = cate.baykeshopcategory_set.all()
    except BaykeShopCategory.DoesNotExist:
        # 没有父级分类
        if not __parent_category().exists():
            return BaykeShopCategory.objects.none()
        # 有父级分类
        queryset = __parent_category().first().baykeshopcategory_set.all()
    return queryset

def __brand_queryset():
    return BaykeShopBrand.objects.all()

@register.simple_tag(name='parent_category_queryset')
def parent_category_queryset():
    return __parent_category()

@register.simple_tag(name='child_category_queryset')
def child_category_queryset(cate_id=None):
    return __child_category(cate_id)

@register.simple_tag(name='brand_queryset')
def brand_queryset():
    return __brand_queryset()


@register.inclusion_tag("baykeshop/tags/sort.html")
def sort_template(request, filter_params:str, sort_field='created_time', **kwargs):
    """排序模板"""
    sort = request.GET.get("sort", "")
    is_asc = sort and sort.startswith("-")
    is_desc = sort and not sort.startswith("-")
    if sort_field == sort:
        sort_field = f"-{sort}"

    return {
        "filter_params": filter_params,
        "request": request,
        "sort_field": sort_field,
        "is_active": sort_field.lstrip('-') == sort.lstrip('-'),
        "is_asc": is_asc,
        "is_desc": is_desc,
        **kwargs
    }

@register.simple_tag
def has_many_sku(spu:BaykeShopGoods):
    """判断商品是否是多规格
    Args:
        spu (BaykeShopGoods): 商品对象
    Returns:
        bool: 是否多规格
    """
    return spu.has_many_sku()

def _group_by_spec(data):
    """
    将数据按规格名称分类

    :param data: 包含规格数据的列表
    :return: 按规格名称分类的字典
    """
    grouped_data = {}

    for item in data:
        spec_name = item['parent__name']
        spec_value = item['name']

        if spec_name not in grouped_data:
            grouped_data[spec_name] = []

        grouped_data[spec_name].append(spec_value)
        grouped_data[spec_name] = list(set(grouped_data[spec_name]))
    return grouped_data

@register.inclusion_tag("baykeshop/tags/sku.html")
def sku_template(spu):
    """商品规格模板"""
    sku_queryset = spu.baykeshopgoodssku_set.order_by('price')
    # 所有的商品规格数据
    specs_data = []

    # 获取sku对应的商品数据
    skus_data = {}
    for sku in sku_queryset:
        specs = json.loads(sku.specs)
        specs_data.extend(specs)
        key = ','.join([spec['name'] for spec in specs]) if specs else 'default'
        skus_data[key] = {
            'id': sku.id,
            'spu_id': sku.goods.id,
            'price': str(sku.price),
            'stock': sku.stock,
            'line_price': str(sku.line_price),
            'sales': sku.sales,
        }
    specs = _group_by_spec(specs_data)
    return {
        "skus_data": skus_data,
        "specs_data": specs,
    }

