from django.forms import widgets
from django.utils.translation import gettext_lazy as _


class Input(widgets.Input):

    template_name = 'baykeshop/forms/widgets/input.html'

    def __init__(self, 
                attrs=None,
                icon_position=None, 
                icons_class=None):
        super().__init__(attrs)
        # 图标位置bk-has-icons-left bk-has-icons-right
        self.icon_position = icon_position or ''
        self.icons_class = icons_class or { 'left': '', 'right': '' }
        
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['icon_position'] = self.icon_position
        context['icons_class'] = self.icons_class
        return context
    
    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs.update({
            'class': 'bk-input'
        })
        return super().build_attrs(base_attrs, extra_attrs)


class TextInput(Input):
    """ 文本输入框 """
    input_type = 'text'
    template_name = 'baykeshop/forms/widgets/text.html'
    

class PasswordInput(Input):
    """ 密码输入框 """

    input_type = 'password'
    template_name = 'baykeshop/forms/widgets/password.html'

    def __init__(self, attrs=None, icon_position=None, icons_class=None, render_value=False):
        super().__init__(attrs, icon_position, icons_class)
        self.render_value = render_value
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['render_value'] = self.render_value
        return context


