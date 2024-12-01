from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import TemplateView, FormView, UpdateView, ListView, CreateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .forms import LoginForm

User = get_user_model()


class BaykeShopUserLoginView(LoginView):
    template_name = 'baykeshop/member/login.html'
    # redirect_authenticated_user = True
    redirect_field_name = 'next'
    next_page = reverse_lazy('shop:list')
    form_class = LoginForm
    extra_context = {
        'title': _('登录'),
    }