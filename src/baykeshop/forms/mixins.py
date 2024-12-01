from django import forms
from django.forms.utils import RenderableFormMixin


class ErrorList(forms.utils.ErrorList):
    """ 错误信息样式  """
    template_name = 'baykeshop/forms/errors.html'


class BaseFormMixins:
    """ 表单样式混入 """
    
    error_css_class = "bk-is-danger"
    required_css_class = "required"

    template_name_bulma = 'baykeshop/forms/default.html'
    template_name_label = 'baykeshop/forms/label.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = ErrorList

    def as_bulma(self):
        return self.render(self.template_name_bulma)