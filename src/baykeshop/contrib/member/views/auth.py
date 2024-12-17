from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from baykeshop.contrib.system.models import BaykeDictModel
from baykeshop.contrib.member.models import BaykeShopUser
from baykeshop.contrib.member.forms import (
    LoginForm, RegisterForm, BaykePasswordResetForm,
    BaykePasswordResetConfirmForm
)

User = get_user_model()


class BaykeShopUserLoginView(SuccessMessageMixin, LoginView):
    """登录页面"""

    template_name = "baykeshop/member/login.html"
    # redirect_authenticated_user = True
    redirect_field_name = "next"
    next_page = reverse_lazy("shop:list")
    form_class = LoginForm
    extra_context = {
        "title": _("登录"),
    }
    success_message = _("登录成功")


class BaykeShopUserRegisterView(FormView):
    """注册页面"""

    template_name = "baykeshop/member/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("member:login")
    extra_context = {
        "title": _("注册"),
    }

    def form_valid(self, form):
        """注册成功"""
        user = form.save()
        BaykeShopUser.objects.create(user=user, nickname=user.username)
        messages.success(self.request, _("注册成功"))
        return super().form_valid(form)


class BaykeShopUserLogoutView(LogoutView):
    """登出页面"""

    next_page = reverse_lazy("member:login")

    def get_success_url(self):
        messages.success(self.request, _("登出成功"))
        return super().get_success_url()


class BaykePasswordResetView(PasswordResetView):
    """重置密码"""
    email_template_name = "baykeshop/member/password_reset_email.html"
    success_url = reverse_lazy("member:password_reset_done")
    template_name = "baykeshop/member/password_reset.html"
    form_class = BaykePasswordResetForm

    
class BaykePasswordResetDoneView(PasswordResetDoneView):
    """重置密码完成"""
    template_name = "baykeshop/member/password_reset_done.html"


class BaykePasswordResetConfirmView(PasswordResetConfirmView):
    """重置密码确认"""
    success_url = reverse_lazy("member:password_reset_complete")
    template_name = "baykeshop/member/password_reset_confirm.html"
    form_class = BaykePasswordResetConfirmForm


class BaykePasswordResetCompleteView(PasswordResetCompleteView):
    """重置密码完成"""
    template_name = "baykeshop/member/password_reset_complete.html"
