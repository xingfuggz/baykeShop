from django.template import Library
from django.utils.safestring import mark_safe

from baykeshop.conf import bayke_settings
from baykeshop.models import admin, product
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


@register.inclusion_tag("baykeshop/public/navbar.html")
def navbar_result():
    return {
        'logo': bayke_settings.PC_LOGO,
        'navs': product.BaykeCategory.get_cates()
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


# @register.inclusion_tag("baykeshop/product/ordering.html")
# def ordering_tag(query, order_field, ):
#     return {
        
#     }




@register.inclusion_tag("baykeshop/product/ordering.html")
def ordering_tag(request, ordering_filed, query, show_name, **kwargs):
    """
    ordering_filed 需要排序的字段名
    query          get请求的额外参数request.query_params
    show_name      对外显示的名称
    kwargs         需要添加到筛选后缀的额外参数
    
    {% load bayke_tags %}
    {% ordering_tag request 'baykeproduct__price' query '价位' categorys=query.categorys %}
    """
    cls_name = "has-text-black-bis"
    href = f"{request.path}"
    icon = ""
    
    if query.get('ordering') == ordering_filed:
        href = f"{href}?ordering=-{ordering_filed}"
        icon = '<span class="mdi mdi-arrow-down"></span>'
    elif query.get('ordering') == f"-{ordering_filed}":
        href = f"{href}?ordering={ordering_filed}"
        icon = '<span class="mdi mdi-arrow-up"></span>'
    else:
        href = f"{href}?ordering={ordering_filed}"
        
    params = []
    if kwargs and query:
        for k, v in kwargs.items():
            if query.get(f'{k}') and f"{k}={v}" not in params:
                params.append(f"{k}={v}")
        
        if not query.get('ordering'):
            href = f'{href}&{"&".join(params)}' 
    
    if f"{ordering_filed}" in request.get_full_path():
        cls_name = "has-text-danger"
    
    return {
        'cls_name': f"{cls_name} mr-2",
        'href': href,
        'icon': icon,
        'show_name': show_name
    }