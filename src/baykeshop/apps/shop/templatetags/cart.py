from django.template import Library

from baykeshop.apps.shop.models import BaykeShopCart

register = Library()


@register.simple_tag
def cart_count(user):
    """获取购物车数量"""
    if not user.is_authenticated:
        return 0
    return BaykeShopCart.get_cart_count(user)