from django.db.utils import IntegrityError
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm
)
from django.utils.translation import gettext_lazy as _

from baykeshop.apps.core.forms.mixin import BaseFormMixin
from .models import UserProfile, UserAddress


class LoginForm(BaseFormMixin, AuthenticationForm):
    """ 登录表单 """
    is_icon = True
    has_icons_left = True
    has_icons_right = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'is-large', 'placeholder': _('请输入用户名')}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'is-large', 'placeholder': _('请输入密码')}
        )
        self.fields['username'].icon_left = 'mdi mdi-account-circle'
        self.fields['username'].icon_right = 'mdi mdi-check'
        self.fields['password'].icon_left = 'mdi mdi-lock'



class RegisterForm(BaseFormMixin, UserCreationForm):
    """注册表单"""
    is_icon = True
    has_icons_left = True
    has_icons_right = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'is-large', 'placeholder': _('请输入用户名')}
        )
        self.fields['password1'].widget.attrs.update(
            {'class': 'is-large','placeholder': _('请输入密码')}
        )
        self.fields['password1'].help_text = _("不能太常见以及全都是数字，至少8个字符。")
        self.fields['password2'].widget.attrs.update(
            {'class': 'is-large','placeholder': _('请再次输入密码')}
        )
        self.fields['username'].icon_left = 'mdi mdi-account-circle'
        self.fields['username'].icon_right = 'mdi mdi-check'
        self.fields['password1'].icon_left = 'mdi mdi-lock'
        self.fields['password2'].icon_left = 'mdi mdi-lock'


class MyPasswordChangeForm(BaseFormMixin, PasswordChangeForm):
    """ 修改密码表单 """
    is_icon = True
    has_icons_left = True 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': _('请输入旧密码')})
        self.fields['new_password1'].widget.attrs.update({'placeholder': _('请输入新密码')})
        self.fields['new_password1'].help_text = _("不能太常见以及全都是数字，至少8个字符。")
        self.fields['new_password2'].widget.attrs.update({'placeholder': _('请再次输入新密码')})
        self.fields['old_password'].icon_left = 'mdi mdi-lock-open'
        self.fields['new_password1'].icon_left = 'mdi mdi-lock'
        self.fields['new_password2'].icon_left = 'mdi mdi-lock'


class UserProfileForm(BaseFormMixin, forms.ModelForm):
    """用户资料表单"""
    is_icon = True
    has_icons_left = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].icon_left = 'mdi mdi-card-account-details-outline'
        self.fields['phone'].icon_left = 'mdi mdi-cellphone'
        self.fields['sex'].icon_left = 'mdi mdi-gender-male-female-variant'

    class Meta:
        model = UserProfile
        fields = ('avatar', 'nickname', 'phone', 'sex')


class UserAddressForm(BaseFormMixin, forms.ModelForm):
    """用户地址表单"""
    is_icon = True
    has_icons_left = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(args, kwargs)
        self.fields['name'].icon_left = 'mdi mdi-account'
        self.fields['phone'].icon_left = 'mdi mdi-cellphone'
        self.fields['detail_address'].icon_left = 'mdi mdi-map-marker-outline'
        self.fields['province'].icon_left = 'mdi mdi-map-marker-outline'
        self.fields['city'].icon_left = 'mdi mdi-map-marker-outline'
        self.fields['district'].icon_left = 'mdi mdi-map-marker-outline'
        self.fields['is_default'].help_text = _("默认地址，将覆盖之前的默认地址。")
        self.fields['province'].widget.attrs.update({'placeholder': _('省份')})
        self.fields['city'].widget.attrs.update({'placeholder': _('城市')})
        self.fields['district'].widget.attrs.update({'placeholder': _('区域')})
        self.fields['detail_address'].widget.attrs.update({'placeholder': _('详细地址')})
        self.fields['name'].widget.attrs.update({'placeholder': _('收件人')})
        self.fields['phone'].widget.attrs.update({'placeholder': _('手机号')})

    class Meta:
        model = UserAddress
        exclude = ('user',)

    def clean_is_default(self):
        is_default = self.cleaned_data.get('is_default')
        if is_default:
            UserAddress.objects.filter(user=self.initial['user'], is_default=True).update(is_default=False)
        return is_default