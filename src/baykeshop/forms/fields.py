from django.forms import fields
from baykeshop.forms import widgets


class RichTextField(fields.CharField):
    """ 富文本编辑器 """

    widget = widgets.RichTextWidget()
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = kwargs.get('widget', self.widget)
        super().__init__(*args, **kwargs)