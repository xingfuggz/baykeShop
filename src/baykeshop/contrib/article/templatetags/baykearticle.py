from django.template import Library

from baykeshop.contrib.article.models import BaykeSidebar


register = Library()

@register.simple_tag
def sidebars():
    """ 侧边栏 """
    return BaykeSidebar.objects.filter(is_show=True).order_by('order')