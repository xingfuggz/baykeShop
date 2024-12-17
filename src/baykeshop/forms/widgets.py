from django.forms import widgets
from django.utils.translation import gettext_lazy as _


class Input(widgets.Input):

    template_name = "baykeshop/forms/widgets/input.html"

    def __init__(self, attrs=None, icon_position=None, icons_class=None):
        super().__init__(attrs)
        # 图标位置bk-has-icons-left bk-has-icons-right
        self.icon_position = icon_position or ""
        self.icons_class = icons_class or {"left": "", "right": ""}

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["icon_position"] = self.icon_position
        context["icons_class"] = self.icons_class
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs.update({"class": "bk-input"})
        return super().build_attrs(base_attrs, extra_attrs)


class TextInput(Input):
    """文本输入框"""

    input_type = "text"
    template_name = "baykeshop/forms/widgets/text.html"


class PasswordInput(Input):
    """密码输入框"""

    input_type = "password"
    template_name = "baykeshop/forms/widgets/password.html"

    def __init__(
        self, attrs=None, icon_position=None, icons_class=None, render_value=False
    ):
        super().__init__(attrs, icon_position, icons_class)
        self.render_value = render_value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["render_value"] = self.render_value
        return context


class Select(widgets.Select):
    """下拉框"""

    template_name = "baykeshop/forms/widgets/select.html"

    def __init__(
        self,
        attrs=None,
        choices=(),
        icon_position=None,
        icons_class=None,
        select_class=None,
    ):
        super().__init__(attrs, choices)
        self.icon_position = icon_position or ""
        # 仅支持左侧配置
        self.icons_class = icons_class or {"left": "", "right": ""}
        # select样式,可以影响颜色，大小，状态
        # bk-is-multiple 支持多选
        # bk-is-rounded 圆角
        # bk-is-link等颜色标签，会影响颜色
        # bk-is-small bk-is-medium bk-is-large 大小
        # bk-is-loading 加载中
        # bk-is-hovered 鼠标移上去
        # bk-is-focused 获取焦点
        # bk-is-active 选中
        self.select_class = select_class or ""

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["icon_position"] = self.icon_position
        context["icons_class"] = self.icons_class
        return context


class RichTextWidget(widgets.Textarea):
    """富文本"""

    template_name = "baykeshop/forms/widgets/richtext.html"

    class Media:
        js = ("baykeshop/tinymce/tinymce.min.js",)
