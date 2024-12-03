from django import forms
from django.template import Library

register = Library()

@register.filter
def is_input(field):
    """判断是否为输入框"""
    return isinstance(field.field, forms.CharField)

@register.filter
def is_select(field):
    """判断是否为下拉框"""
    return isinstance(field.field, forms.TypedChoiceField)

@register.filter
def is_image(field):
    """判断是否为图片上传框"""
    return isinstance(field.field, forms.ImageField)

@register.filter
def is_boolean(field):
    """判断是否为状态选择框"""
    return isinstance(field.field, forms.BooleanField)

@register.filter
def add_class(field, css_class):
    """为表单项添加css类"""
    if 'class' in field.field.widget.attrs:
        field.field.widget.attrs['class'] = ' '.join([field.field.widget.attrs['class'], css_class])
    else:
        field.field.widget.attrs['class'] = css_class
    return field

def change_template(field, template_name):
    """修改表单项的模板"""
    field.field.widget.template_name = template_name
    return field