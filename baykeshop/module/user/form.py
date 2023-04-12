from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.html import format_html_join, format_html
from django.core.exceptions import ValidationError

from baykeshop.conf import bayke_settings
from baykeshop.module.user.models import BaykeUserInfo

User = get_user_model()

def _password_validators_help_text_html(password_validators=None):
    """
    Return an HTML string with all help texts of all configured validators
    in an <ul>.
    """
    help_texts = password_validation.password_validators_help_texts(password_validators)
    help_items = format_html_join('', '<p>{}</p>', ((help_text,) for help_text in help_texts))
    return format_html('<div class="help">{}</div>', help_items) if help_items else ''

password_validators_help_text_html = lazy(_password_validators_help_text_html, str)


class BaykeShopUsernameField(UsernameField):

    def widget_attrs(self, widget):
        return {
            'class': 'input',
            'placeholder':'请输入用户名...',
            **super().widget_attrs(widget)
        }
        
        
class LoginForm(AuthenticationForm):
    """ 登录表单 """
    username = UsernameField(
        widget=forms.TextInput(attrs={
            "autofocus": True, 
            "class": "input", 
            "placeholder":" 请输入用户名..."
        }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password", 
            "class": "input", 
            "placeholder":" 请输入密码..."
        }),
    )


class RegisterForm(UserCreationForm):
    """ 注册用户表单 """
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 
            'class': 'input', 
            "placeholder":" 请输入密码..."
        }),
        help_text=password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password', 
            'class': 'input',
            "placeholder":" 请再次输入密码..."
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': BaykeShopUsernameField}
        
        
class UserForm(forms.ModelForm):
    """ 用户信息表单 """
    class Meta:
        model = User
        fields = ['email',]


class UpdateUserInfoForm(forms.ModelForm):
    """ 用户关联信息表单 """
    class Meta:
        model = BaykeUserInfo
        fields = ['owner', 'avatar', 'phone', 'balance', 'nickname']
  
    def clean_phone(self):
        import re
        phone = self.cleaned_data['phone']
        reg = re.compile(bayke_settings.PHONE_REGX)
        if (phone is not None) and (not reg.search(phone)):
            raise ValidationError("手机号格式有误！")
        return phone