from django import forms
from django.utils.translation import gettext_lazy as _

from baykeshop.apps.core.forms.mixin import BaseFormMixin
from .models import BaykeShopCart, BaykeShopSKU


class BaykeShopCartAddForm(forms.Form):
    """购物车添加表单"""
    num = forms.IntegerField(min_value=1, max_value=999, initial=1, label=_('数量'))
    sku_id = forms.IntegerField(min_value=1, label=_('商品'))

    def clean__sku_id(self, sku_id):
        try:
            BaykeShopSKU.objects.get(id=sku_id)
        except BaykeShopSKU.DoesNotExist:
            raise forms.ValidationError(_('商品不存在'))
        return sku_id


class BaykeShopCartForm(forms.ModelForm):
    """购物车表单"""
    class Meta:
        model = BaykeShopCart
        fields = ['num']


class SearchForm(forms.Form):
    """搜索表单"""

    keyword = forms.CharField(
        max_length=50,
        required=False, 
        label=_('关键字'), 
        widget=forms.TextInput(attrs={'placeholder': _('请输入商品关键字'), 'class': 'input is-large'}),
    )
