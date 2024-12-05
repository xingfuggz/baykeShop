from django.template import Library
from baykeshop.contrib.system.models import Visit, BaykeBanners, BaykeDictModel

register = Library()

@register.simple_tag
def dict_value(key):
    """获取字典值"""
    return BaykeDictModel.get_key_value(key)

@register.simple_tag
def visit_count(content_object:Visit, key:str):
    """访问统计"""
    return Visit.objects.get_uv_pv_count(content_object).get(key)


@register.inclusion_tag("baykeshop/tags/banners.html")
def banners_template():
    """ 轮播图 """
    return {
        'banners': BaykeBanners.objects.filter(is_show=True)
    }