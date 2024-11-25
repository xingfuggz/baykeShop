from django.template import Library
from django.urls import reverse
from baykeshop.apps.order.models import BaykeShopOrder, BaykeShopOrderComment


register = Library()

def _insert_update_url(data, request):
    """ 插入修改地址url
    方便修改地址后能快速跳转回原地址
    """
    for item in data:
        item['update_url'] = f"{reverse('user:address-update', kwargs={'pk': item['id']})}?next={request.get_full_path()}"
    return data

@register.inclusion_tag('order/address.html', takes_context=True)
def address_template(context, user):
    address_list = user.address.values()
    request = context['request']
    return {
        'address_list': _insert_update_url(list(address_list), request),
        'request': request,
    }

@register.inclusion_tag('order/paytype.html')
def paytype_template():
    choices = BaykeShopOrder.PayType.choices
    _types = [
        { 
            'value': item[0], 
            'label': item[1]
        } 
        for item in choices
    ]
    return { 'pay_types': _types }

@register.simple_tag
def comment_rate(spu):
    return BaykeShopOrderComment.get_spu_comment_avg_score(spu)