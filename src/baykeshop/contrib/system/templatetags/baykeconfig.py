from django.template import Library
from baykeshop.contrib.system.models import BaykeDictModel

register = Library()

@register.simple_tag
def dict_value(key):
    """获取字典值"""
    return BaykeDictModel.get_key_value(key)