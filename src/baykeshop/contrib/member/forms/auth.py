import logging

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.template import loader
from django.core.mail import get_connection
from django.core.mail import EmailMultiAlternatives

from baykeshop.contrib.system.models import BaykeDictModel
from baykeshop.forms.mixins import BaseFormMixins
from baykeshop.forms import widgets

logger = logging.getLogger("baykeshop.contrib.member")


class LoginForm(BaseFormMixins, AuthenticationForm):
    """登录表单"""

    username = forms.CharField(
        label=_("用户名"),
        widget=widgets.TextInput(
            attrs={"placeholder": _("请输入用户名"), "autofocus": True},
            icon_position="bk-has-icons-left bk-has-icons-right",
            icons_class={"left": "mdi mdi-account", "right": "mdi mdi-check"},
        ),
        required=True,
    )
    password = forms.CharField(
        label=_("密码"),
        widget=widgets.PasswordInput(
            attrs={"placeholder": _("请输入密码")},
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        ),
        required=True,
    )


class RegisterForm(BaseFormMixins, UserCreationForm):
    """注册表单"""

    username = forms.CharField(
        label=_("用户名"),
        strip=False,
        widget=widgets.TextInput(
            attrs={"placeholder": _("请输入用户名"), "autofocus": True},
            icon_position="bk-has-icons-left bk-has-icons-right",
            icons_class={"left": "mdi mdi-account", "right": "mdi mdi-check"},
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=widgets.PasswordInput(
            attrs={"placeholder": _("请输入密码"), "autocomplete": "new-password"},
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=widgets.PasswordInput(
            attrs={"placeholder": _("请再次输入密码")},
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        ),
        help_text=_("Enter the same password as before, for verification."),
    )


class ChangePasswordForm(BaseFormMixins, PasswordChangeForm):
    """修改密码表单"""

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=widgets.PasswordInput(
            attrs={
                "placeholder": _("请输入旧密码"),
                "autocomplete": "current-password",
            },
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=widgets.PasswordInput(
            attrs={"placeholder": _("请输入新密码"), "autocomplete": "new-password"},
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=widgets.PasswordInput(
            attrs={
                "placeholder": _("请再次输入新密码"),
                "autocomplete": "new-password",
            },
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        ),
        help_text=_("Enter the same password as before, for verification."),
    )


class BaykePasswordResetForm(BaseFormMixins, PasswordResetForm):
    """重置密码表单"""

    email = forms.EmailField(
        label=_("邮箱"),
        widget=widgets.TextInput(
            attrs={
                "placeholder": _("请输入邮箱"),
                "autocomplete": "email",
                "type": "email",
            },
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-email", "right": ""},
        ),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        # 指定邮件发送服务器
        # DEVELOP_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
        PRODUCTION_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
        from_email = BaykeDictModel.get_key_value("EMAIL_HOST_USER")
        connection = get_connection(
            fail_silently=False,
            host=BaykeDictModel.get_key_value("EMAIL_HOST"),
            port=int(BaykeDictModel.get_key_value("EMAIL_PORT")),
            username=BaykeDictModel.get_key_value("EMAIL_HOST_USER"),
            password=BaykeDictModel.get_key_value("EMAIL_HOST_PASSWORD"),
            use_ssl=BaykeDictModel.get_key_value("EMAIL_USE_SSL"),
            from_email=from_email,
            backend=PRODUCTION_EMAIL_BACKEND
        )
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email], connection=connection)
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        try:
            email_message.send()
        except Exception:
            logger.exception(
                "Failed to send password reset email to %s", context["user"].pk
            )


class BaykePasswordResetConfirmForm(BaseFormMixins, SetPasswordForm):
    """重置密码确认表单"""

    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=widgets.PasswordInput(
            attrs={"placeholder": _("请输入新密码"), "autocomplete": "new-password"},
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        )
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=widgets.PasswordInput(
            attrs={
                "placeholder": _("请再次输入新密码"),
                "autocomplete": "new-password",
            },
            icon_position="bk-has-icons-left",
            icons_class={"left": "mdi mdi-lock", "right": ""},
        )
    )