from django import forms
from django.forms.utils import RenderableFormMixin


class BaseFormMixins:
    """ 表单样式混入 """
    template_name_bulma = 'baykeshop/forms/default.html'
    template_name_label = 'baykeshop/forms/label.html'

    def as_bulma(self):
        return self.render(self.template_name_bulma)