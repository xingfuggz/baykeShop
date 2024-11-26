from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget


class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, AdminTextareaWidget):
                field.widget.attrs['rows'] = 3