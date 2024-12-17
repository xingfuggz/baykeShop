from django import forms
from django.utils.translation import gettext_lazy as _

from baykeshop.forms.mixins import BaseFormMixins
from baykeshop.forms import widgets
from baykeshop.contrib.shop.models import BaykeShopOrdersComment
from baykeshop.contrib.member.models import BaykeShopUserAddress, BaykeShopUser
 

class BaykeShopUserAddressForm(BaseFormMixins, forms.ModelForm):
    """ 收货地址表单 """
    
    class Meta:
        model = BaykeShopUserAddress
        fields = ['name', 'phone', 'province', 'city', 'district', 'address', 'is_default']
        widgets = {
            'name': widgets.TextInput(
                attrs={'placeholder': _('请输入收货人')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-account', 'right': ''}
            ),
            'phone': widgets.TextInput(
                attrs={'placeholder': _('请输入手机')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-phone', 'right': ''}
            ),
            'province': widgets.TextInput(
                attrs={'placeholder': _('请输入省')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-map-marker', 'right': ''}
            ),
            'city': widgets.TextInput(
                attrs={'placeholder': _('请输入市')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-map-marker', 'right': ''}
            ),
            'district': widgets.TextInput(
                attrs={'placeholder': _('请输入区')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-map-marker', 'right': ''}
            ),
            'address': widgets.TextInput(
                attrs={'placeholder': _('请输入详细地址')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-map-marker', 'right': ''}
            )
        }


class BaykeShopUserProfileForm(BaseFormMixins, forms.ModelForm):
    """ 个人资料表单 """
    
    email = forms.EmailField(
        label=_("邮箱"),
        widget=widgets.TextInput(
            attrs={'placeholder': _('请输入邮箱'), "autocomplete": "email", 'type': 'email'},
            icon_position='bk-has-icons-left',
            icons_class={'left': 'mdi mdi-email', 'right': ''}
        )
    )

    class Meta:
        model = BaykeShopUser
        fields = ['avatar', 'gender', 'nickname', 'birthday', 'email', 'mobile', 'qq', 'wechat', 'description']
        widgets = {
            'nickname': widgets.TextInput(
                attrs={'placeholder': _('请输入昵称')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-account', 'right': ''},
            ),
            'mobile': widgets.TextInput(
                attrs={'placeholder': _('请输入手机号码')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-phone', 'right': ''}
            ),
            'gender': widgets.Select(
                attrs={'placeholder': _('请选择性别')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-gender-male-female', 'right': ''}
            ),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'bk-input' }, format='%Y-%m-%d'),
            'qq': widgets.TextInput(
                attrs={'placeholder': _('请输入QQ')},
               icon_position='bk-has-icons-left',
               icons_class={'left': 'mdi mdi-qqchat', 'right': ''}
            ),
            'wechat': widgets.TextInput(
                attrs={'placeholder': _('请输入微信')},
                icon_position='bk-has-icons-left',
                icons_class={'left': 'mdi mdi-wechat', 'right': ''}
            ),
            'description': forms.Textarea(
                attrs={'placeholder': _('请输入简介'), 'class': 'bk-textarea bk-has-fixed-size'},
            )
        }


class BaykeShopOrdersCommentForm(BaseFormMixins, forms.ModelForm):
    """订单评论表单"""

    class Meta:
        model = BaykeShopOrdersComment
        fields = ('content', 'score',)
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': _('请输入评论内容'), 'class': 'bk-textarea', 'rows': 5, 'cols': 50},
            ),
            'score': widgets.Select(
                attrs={'placeholder': _('请选择评分')},
                icon_position='bk-has-icons-left',
                icons_class={'left':'mdi mdi-star', 'right': ''}
            )
        }