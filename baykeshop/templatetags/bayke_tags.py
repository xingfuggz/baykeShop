from django.template import Library
from django.urls import reverse, NoReverseMatch

from baykeshop.conf import bayke_settings
from baykeshop.models import admin, product, cart
from baykeshop.conf import bayke_settings


register = Library()


@register.simple_tag
def breadcrumbs(request, opts=None):
    if bayke_settings.ADMIN_MENUS:
        if opts:
            p = admin.BaykePermission.objects.filter(
                permission__content_type__app_label=opts.app_label,
                permission__content_type__model=opts.model_name
            )
            request.breadcrumbs = {
                p.first().menus.name: {
                    'name': str(opts.verbose_name_plural), 
                    'url': request.path
                }
            }
            return request.breadcrumbs
        return request.breadcrumbs
    else:
        return None
    

@register.inclusion_tag("baykeshop/public/banners.html")
def carousel(banners:list):
    return {"banners": banners}


@register.inclusion_tag("baykeshop/public/navbar.html", takes_context=True)
def navbar_result(context):
    request = context['request']
    try:
        query = request.query_params.dict()
    except AttributeError:
        query = request.GET.dict()
        
    search_value = query.get('search', '')
    categorys = query.get('categorys', '') if bayke_settings.HAS_SEARCH_CATEGORY else ''
    return {
        'logo': bayke_settings.PC_LOGO,
        'navs': product.BaykeCategory.get_cates(),
        'search_value': search_value,
        'search_action':f'{reverse("baykeshop:goods-list")}',
        'categorys': categorys
    } 
    
    
@register.inclusion_tag("baykeshop/public/head_top.html")
def head_top(request):
    return {
        'cartsnum': cart.BaykeShopingCart.get_cart_count(request.user) if request.user.is_authenticated else 0,
        'request': request
    }
    

@register.inclusion_tag("baykeshop/public/spu_box.html")
def spu_box(spu):
    if spu.get('baykeproduct_set'):
        spu['price'] = spu.get('baykeproduct_set')[0].get('price')
        spu['sales'] = sum([ product.get('sales', 0) for product in spu.get('baykeproduct_set')])
    return {"spu": spu}


@register.simple_tag
def strtoint(strnum:str):
    """ 将一个数字字符串转为int """
    if strnum and strnum.isdigit():
        return int(strnum)


@register.simple_tag
def inttostr(intnum:str):
    """ 将一个数字转为str类型 """
    if isinstance(intnum, int):
        return str(intnum)


@register.inclusion_tag("baykeshop/public/pages.html")
def pages(request, datas):
    """ 分页小组件 """
    params = []
    query = request.query_params.dict()
    
    try:
        page = query.pop('page')
    except KeyError:
        pass
    
    for k, v in query.items():
        if f"{k}={v}" not in params:
            params.append(f"{k}={v}")
    params = '&'.join(params)
    return {'datas': datas, 'params': params}

    
@register.inclusion_tag("baykeshop/product/ordering.html")
def ordering_tag(request, order_field, show_name):
    
    """
    order_field    需要排序的字段名
    show_name      对外显示的名称
    
    {% load bayke_tags %}
    {% ordering_tag request 'baykeproduct__price' '价位' %}
    """
    
    icon = ""
    cls_name = "has-text-black-bis"
    query = request.query_params.dict()
    params = []
    ordering = ""
    
    try:
        ordering = query.pop('ordering')
    except KeyError:
        pass
    
    for k, v in query.items():
        if f"{k}={v}" not in params:
            params.append(f"{k}={v}")
    href = f"?ordering={order_field}&{'&'.join(params)}"
    if ordering == f'{order_field}':
        href = f"?ordering=-{order_field}&{'&'.join(params)}"
        icon = '<span class="mdi mdi-arrow-down"></span>'
    elif ordering == f'-{order_field}':
        icon = '<span class="mdi mdi-arrow-up"></span>'
    
    # 判断是否选中
    if f"{order_field}" in request.get_full_path():
        cls_name = "has-text-danger"

    return {
        'href': href,
        'icon': icon,
        'cls_name': f"{cls_name} mr-2",
        'show_name': show_name
    }


@register.inclusion_tag("baykeshop/product/banners.html")
def spu_banners(banners):
    return {
        'banners': banners
    }
    

@register.inclusion_tag("baykeshop/user/address.html")
def address_result(address:list, update=False, delete=False):
    return {
        'address': address,
        'update': update,
        'delete': delete
    }
    

@register.inclusion_tag("baykeshop/payment/pay_methods.html")
def pay_methods(request, methods):
    # 支付方式组件
    return {
        'methods': methods,
        'request': request
    }
    
@register.inclusion_tag("baykeshop/order/action.html")
def orderinfo_action(order):

    return {
        'ordergoods_count': sum([good['count'] for good in order['baykeordergoods_set']]),
        'is_commented':all([good['is_commented'] for good in order['baykeordergoods_set']]),
        'order': order
    }