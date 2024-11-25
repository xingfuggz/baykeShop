from django import forms
from django.utils.translation import gettext_lazy as _

from baykeshop.apps.core.forms.mixin import BaseFormMixin
from .models import BaykeShopOrderComment

class BaykeShopOrderCreateForm(forms.Form):
    """ 创建订单 表单 """
    sku_ids = forms.CharField(
        required=True, 
        max_length=100, 
        min_length=1, 
        help_text=_('商品ID,多个以英文逗号隔开')
    )
    source = forms.CharField(
        required=True, 
        max_length=50, 
        initial='detail', 
        help_text=_('购买来源,详情页购买:detail,购物车购买:cart')
    )
    count = forms.IntegerField(required=False, help_text=_('购买数量'))
    receiver = forms.CharField(required=True, max_length=50, label=_('收货人'))
    address = forms.CharField(required=True, max_length=100, label=_('收货地址'))
    phone = forms.CharField(required=True, max_length=11, label=_('联系电话'))


class BaykeShopOrderCommentForm(BaseFormMixin, forms.ModelForm):
    """ 订单评价表单 """
    
    class Meta:
        model = BaykeShopOrderComment
        fields = ['content', 'score', 'satisfaction']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'textarea', 
                'placeholder': _('请输入评价内容'), 
                'rows': 3
            }),
        }