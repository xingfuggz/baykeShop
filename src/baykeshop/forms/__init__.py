from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget


class Form(forms.Form):
    pass


class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # print(field.widget)
            if isinstance(field.widget, AdminTextareaWidget):
                field.widget.attrs['rows'] = 3
            
            # if isinstance(field, forms.JSONField):
            #     print('json', field.widget)
                # field.widget.attrs['class'] = 'json-editor'