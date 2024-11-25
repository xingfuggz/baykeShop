from django.utils.translation import gettext_lazy as _
from django.forms import widgets

from baykeshop.config import bayke_settings


class QuillWidget(widgets.Widget):
    """
    富文本编辑器
    """
    template_name = 'core/forms/widgets/quill.html'

    def __init__(self, attrs=None, modules=None):
        super().__init__(attrs)
        self.defaults = bayke_settings.QUILL_CONFIGS['DEFAULT']
        self.modules = modules or self.defaults.get('modules')

    class Media:
        css = bayke_settings.QUILL_CONFIGS.get('CSS')
        js = bayke_settings.QUILL_CONFIGS.get('JS')

    def get_modules(self):
        return self.modules
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['modules'] = self.get_modules()
        context['widget']['placeholder'] = _('请输入内容')
        context['widget']['theme'] = self.defaults.get('theme')
        return context