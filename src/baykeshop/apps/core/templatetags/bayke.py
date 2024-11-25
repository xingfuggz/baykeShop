'''
@file            :bayke.py
@Description     :模版标签及过滤器
@Date            :2024/11/03 19:50:15
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''
from django.template import Library
from django.utils.safestring import mark_safe

from baykeshop.apps.core.utils.config import SiteConfig
from baykeshop.apps.core.models import Visit

register = Library()
site_config = SiteConfig()

@register.simple_tag
def paginator_range(page_obj, on_each_side=1):
    """分页导航条"""
    return page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=on_each_side)

@register.inclusion_tag("core/pagination.html")
def paginator_template(page_obj, request):
    """分页导航条"""
    params = request.GET.copy()
    params.pop("page", None)
    return {
        "urlencode": params.urlencode(),
        "page_obj": page_obj
    }

@register.simple_tag
def config(field_name:str):
    """获取站点配置"""
    return site_config.get_site_extend_value(field_name)

@register.simple_tag
def site_config_value(key:str):
    """获取站点配置"""
    return site_config.get_site_config_value(key)


@register.simple_tag
def render_charts_template(embed:str):
    """图表模板"""
    return mark_safe(embed)

@register.simple_tag
def visit_count(content_object:Visit, key:str):
    """访问统计"""
    return Visit.objects.get_uv_pv_count(content_object).get(key)