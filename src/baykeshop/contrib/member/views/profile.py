from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import RedirectURLMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, FormView, UpdateView, ListView, CreateView, DeleteView

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from baykeshop.contrib.member.models import BaykeShopUserAddress, BaykeShopUser
from baykeshop.contrib.member.forms import ChangePasswordForm, BaykeShopUserAddressForm, BaykeShopUserProfileForm

class BaykeShopUserProfileView(LoginRequiredMixin, TemplateView):
    """ 个人中心 """
    template_name = 'baykeshop/member/profile.html'
    extra_context = {'title': _('个人中心'),}
    

class BaykeShopUserPasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    """ 修改密码 """
    template_name = 'baykeshop/member/password.html'
    extra_context = {'title': _('修改密码'),}
    success_url = reverse_lazy('member:profile')
    login_url = reverse_lazy('member:login')
    form_class = ChangePasswordForm
    success_message = _('密码修改成功')


class BaykeShopUserAddressListView(LoginRequiredMixin, ListView):
    """ 收货地址列表 """
    template_name = 'baykeshop/member/address_list.html'
    model = BaykeShopUserAddress
    context_object_name = 'address_list'
    extra_context = {'title': _('收货地址列表'),}
    login_url = reverse_lazy('member:login')
    
    def get_queryset(self):
        return BaykeShopUserAddress.objects.filter(user=self.request.user)
    

class BaykeShopUserAddressCreateView(LoginRequiredMixin, SuccessMessageMixin, RedirectURLMixin, CreateView):
    """ 新增收货地址 """
    template_name = 'baykeshop/member/address_form.html'
    model = BaykeShopUserAddress
    form_class = BaykeShopUserAddressForm
    extra_context = {'title': _('新增收货地址'),}
    login_url = reverse_lazy('member:login')
    success_url = reverse_lazy('member:address-list')
    success_message = _('新增收货地址成功')
    redirect_field_name = 'next'

    def get_queryset(self):
        return BaykeShopUserAddress.objects.filter(user=self.request.user)
    
    def get_redirect_url(self):
        return self.request.GET.get(self.redirect_field_name) or self.success_url

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.cleaned_data['is_default']:
            BaykeShopUserAddress.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
        return super().form_valid(form)
    

class BaykeShopUserAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, RedirectURLMixin, UpdateView):
    """ 修改收货地址 """
    template_name = 'baykeshop/member/address_form.html'
    model = BaykeShopUserAddress
    form_class = BaykeShopUserAddressForm
    extra_context = {'title': _('修改收货地址'),}
    login_url = reverse_lazy('member:login')
    success_url = reverse_lazy('member:address-list')
    success_message = _('修改收货地址成功')
    redirect_field_name = 'next'

    def get_redirect_url(self):
        return self.request.GET.get(self.redirect_field_name) or self.success_url
    
    def get_queryset(self):
        return BaykeShopUserAddress.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.cleaned_data['is_default']:
            BaykeShopUserAddress.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
        return super().form_valid(form)
    

class BaykeShopUserAddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """ 删除收货地址 """
    model = BaykeShopUserAddress
    success_url = reverse_lazy('member:address-list')
    success_message = _('删除收货地址成功')
    login_url = reverse_lazy('member:login')
    
    def get_queryset(self):
        return BaykeShopUserAddress.objects.filter(user=self.request.user)


class BaykeShopUserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """ 修改个人资料 """
    template_name = 'baykeshop/member/profile_form.html'
    model = BaykeShopUser
    form_class = BaykeShopUserProfileForm
    extra_context ={'title': _('修改个人资料'),}
    login_url = reverse_lazy('member:login')
    success_url = reverse_lazy('member:profile')
    success_message = _('修改个人资料成功')

    def get_object(self):
        instance, iscreated = BaykeShopUser.objects.get_or_create(
            user=self.request.user, defaults={
                'user': self.request.user,
                'nickname': self.request.user.username
            })
        return instance
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['email'] = self.request.user.email
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.cleaned_data['email']:
            user = self.request.user
            user.email = form.cleaned_data['email']
            user.save()
        return super().form_valid(form)
