from django.forms import widgets
# widgets.JSONField.template_name = 'widgets/json.html'
import json

class GalleryWidget(widgets.Textarea):
    '''
    自定义Widget
    '''
    template_name = 'baykeshop/widgets/gallery.html'

    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs, **kwargs)
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context