from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm
)
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from baykeshop.forms.mixins import BaseFormMixins
from baykeshop.forms import widgets
from baykeshop.contrib.shop.models import BaykeShopOrdersComment
from .models import BaykeShopUserAddress, BaykeShopUser


class LoginForm(BaseFormMixins, AuthenticationForm):
    """ 登录表单 """
    username = forms.CharField(
        label=_('用户名'),
        widget=widgets.TextInput(
            attrs={'placeholder': _('请输入用户名'), 'autofocus': True},
            icon_position='bk-has-icons-left bk-has-icons-right',
            icons_class={'left': 'mdi mdi-account', 'right': 'mdi mdi-check'}
        ),
        required=True,
    )
    password = forms.CharField(
        label=_('密码'),
        widget=widgets.PasswordInput(
            attrs={'placeholder': _('请输入密码')},
            icon_position='bk-has-icons-left',
            icons_class={'left': 'mdi mdi-lock', 'right': ''}
        ),
        required=True,
    )


class RegisterForm(BaseFormMixins, UserCreationForm):
    """ 注册表单 """

    username = forms.CharField(
        label=_("用户名"),
        strip=False,
        widget=widgets.TextInput(
            attrs={'placeholder': _('请输入用户名'), "autofocus": True},
            icon_position='bk-has-icons-left bk-has-icons-right',
            icons_class={'left': 'mdi mdi-account', 'right': 'mdi mdi-check'}
        )
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=widgets.PasswordInput(
            attrs={'placeholder': _('请输入密码'), "autocomplete": "new-password"},
            icon_position='bk-has-icons-left',
            icons_class={'left': 'mdi mdi-lock', 'right': ''}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=widgets.PasswordInput(
            attrs={'placeholder': _('请再次输入密码')},
            icon_position='bk-has-icons-left',
            icons_class={'left': 'mdi mdi-lock', 'right': ''}
        ),
        help_text=_("Enter the same password as before, for verification."),
    )


class ChangePasswordForm(BaseFormMixins, PasswordChangeForm):
    """ 修改密码表单 """

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=widgets.PasswordInput(
            attrs={'placeholder': _('请输入旧密码'), "autocomplete": "current-password"},
            icon_position='bk-has-icons-left',
            icons_class={'left': 'mdi mdi-lock', 'right': ''}
        )
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=widgets.PasswordInput(
            attrs={'placeholder': _('请输入新密码'), "autocomplete": "new-password"},
            icon_position='bk-has-icons-left',
            icons_class={'left': 'mdi mdi-lock', 'right': ''}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=widgets.PasswordInput(
            attrs={'placeholder': _('请再次输入新密码'), "autocomplete": "new-password"},
            icon_position='bk-has-icons-left',
            icons_class={'left': 'mdi mdi-lock', 'right': ''}
        ),
        help_text=_("Enter the same password as before, for verification."),
    )
        

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