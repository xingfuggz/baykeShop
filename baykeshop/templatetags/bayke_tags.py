from django.template import Library

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

    