from django import forms
from django.forms.utils import RenderableMixin


class BaseFormMixin(RenderableMixin):
    
    # 显示图标
    is_icon = False
    # 是否显示左边的图标
    has_icons_left = False
    # 是否显示右边的图标
    has_icons_right = False
    # 是否显示label
    has_label = True
    # 自定义模板
    template_name_bulma = 'core/forms/bulma.html'

    def as_bulma(self):
        return self.render(template_name=self.template_name_bulma)

    def get_context(self):
        context = super().get_context()
        context['is_icon'] = self.is_icon
        context['has_icons_left'] = self.has_icons_left
        context['has_icons_right'] = self.has_icons_right
        context['has_label'] = self.has_label
        return context

