from django.db.utils import IntegrityError
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm
)
from django.utils.translation import gettext_lazy as _

from baykeshop.forms.mixins import BaseFormMixins
from baykeshop.forms import widgets


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
    
    