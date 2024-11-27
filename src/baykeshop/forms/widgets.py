from django.forms import widgets


class Widget(widgets.Widget):
    """
    自定义Widget
    """
    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs, **kwargs)
        

class SpecSelectWidget(widgets.TextInput):
    """
    自定义JsonWidget
    """
    template_name = 'shop/widgets/json.html'



