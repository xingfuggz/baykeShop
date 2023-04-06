from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class BaseModelAdmin(admin.ModelAdmin):
    """继承了django的ModelAdmin
    重写并新增了一些全局方法
    """
    change_list_template = "baykeadmin/change_list.html"
    change_form_template = "baykeadmin/change_form.html"
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.model._meta.model_name not in ['user', 'group', 'permission', 'logentry']:
            queryset = queryset.filter(is_del=False)
        return queryset
    
    def change_view(self, request, object_id, form_url="", extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context)
    
    @admin.display(description="操作")
    def operate(self, obj):
        hs = '<a href="{}">编辑</a> | <a href="{}">删除</a>'
        h1 = reverse(f'baykeadmin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(obj.pk, ))
        h2 = reverse(f'baykeadmin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=(obj.pk, ))
        return format_html(hs, h1, h2)
    