from django.template import Library

from baykeshop.conf import bayke_settings
from baykeshop.models import admin, product
from baykeshop.conf import bayke_settings
from baykeshop.models.context import BaykeModelContext


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