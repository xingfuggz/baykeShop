from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import TemplateView, FormView, UpdateView, ListView, CreateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

# Create your views here.
from .forms import (
    LoginForm, RegisterForm, MyPasswordChangeForm, 
    UserProfileForm, UserAddressForm
)
from .models import UserProfile, UserAddress

User = get_user_model()


class BaykeShopLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm
    next_page = reverse_lazy('user:account')
    extra_context = {
        'title': _('登录'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


class BaykeShopLogoutView(LogoutView):
    """ 退出登录 """
    http_method_names = ['get', 'post', 'options']
    next_page = reverse_lazy('shop:spu-list')
    template_name = 'user/logout.html'
    next_page = reverse_lazy('user:login')
    extra_context = {
        'title': _('退出')
    }

    def get(self, request, *args, **kwargs):
        """ 这个方法为了兼容低版本，未来可能不再支持 """
        return super().post(request, *args, **kwargs)


class BaykeShopRegisterView(FormView):
    """
    注册视图
    """
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user:account')
    extra_context = {
        'title': _('注册'),
    }

    def form_valid(self, form):
        user = form.save()
        UserProfile.objects.create(user=user)
        return super().form_valid(form)


class BaykeShopAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'
    login_url = reverse_lazy('user:login')
    extra_context = {
        'title': _('我的账户')
    }


class BaykeShopPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """ 修改密码 """
    template_name = 'user/password_change.html'
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('user:account')
    login_url = reverse_lazy('user:login')
    extra_context = {
        'title': _('修改密码')
    }


class BaykeShopUserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ 用户资料 """
    model = UserProfile
    template_name = 'user/profile_change.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('user:account')

    def get_object(self, queryset=None):
        """ 重写获取对象 """
        try:
            self.request.user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=self.request.user)
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('修改我的资料')
        return context


class BaykeShopUserAddressView(LoginRequiredMixin, ListView):
    """ 用户地址 """
    template_name = 'user/address.html'
    login_url = reverse_lazy('user:login')
    context_object_name = 'address_list'

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('我的地址')
        return context


class BaykeShopUserAddressCreateView(LoginRequiredMixin, CreateView):
    """ 新增地址 """
    model = UserAddress
    template_name = 'user/address_create.html'
    form_class = UserAddressForm
    success_url = reverse_lazy('user:address-list')
    login_url = reverse_lazy('user:login')
    extra_context = {
        'title': _('新增地址')
    }

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        params = self.request.GET.dict()
        if params.get('next'):
            next = params.pop('next', None)
            _params = '&'.join([f"{key}={value}" for key, value in params.items()])
            success_url = f"{next}&{_params}"
            return success_url
        return super().get_success_url()
    

class BaykeShopUserAddressUpdateView(LoginRequiredMixin, UpdateView):
    """ 修改地址 """
    model = UserAddress
    template_name = 'user/address_change.html'
    form_class = UserAddressForm
    success_url = reverse_lazy('user:address-list')
    login_url = reverse_lazy('user:login')
    extra_context = {
        'title': _('修改地址')
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_success_url(self):
        params = self.request.GET.dict()
        if params.get('next'):
            next = params.pop('next', None)
            _params = '&'.join([f"{key}={value}" for key, value in params.items()])
            success_url = f"{next}&{_params}"
            return success_url
        return super().get_success_url()
    

class UserAddressDeleteView(LoginRequiredMixin, DeleteView):
    """ 删除地址 """
    model = UserAddress
    success_url = reverse_lazy('user:address-list')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)