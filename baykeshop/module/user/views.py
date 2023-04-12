from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)

from baykeshop.conf import bayke_settings
from baykeshop.module.user.form import LoginForm, RegisterForm
from baykeshop.module.user.models import BaykeUserInfo


class LoginView(SuccessMessageMixin, BaseLoginView):
    """ 登录 """
    next_page = bayke_settings.LOGIN_NEXT_PAGE
    form_class = LoginForm
    redirect_field_name = 'redirect_to'
    template_name = "baykeshop/user/login.html"
    success_message = "%(username)s 登录成功！"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )
        

class LogoutView(BaseLogoutView):
    """ 登出 """
    template_name = 'baykeshop/user/logout.html'
    

class RegisterView(SuccessMessageMixin, FormView):
    """ 注册用户 """
    template_name = 'baykeshop/user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("baykeshop:home")
    success_message = "%(username)s 注册成功，已登录！"
    
    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            auth_user = authenticate(username=new_user.username, 
                                     password=form.cleaned_data['password1'])
            BaykeUserInfo.objects.create(owner=auth_user, nickname=auth_user.username)
            login(self.request, auth_user)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )
        