from django.db import models

from baykeshop.forms.widgets import RichTextWidget


class RichTextField(models.TextField):
    
    def formfield(self, **kwargs):
        kwargs['widget'] = RichTextWidget
        return super().formfield(**kwargs)
    