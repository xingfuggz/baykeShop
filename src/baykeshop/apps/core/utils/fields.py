from django.db.models.fields import TextField

from baykeshop.apps.core.forms.widgets import QuillWidget


class RichTextField(TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = QuillWidget
        return super().formfield(**kwargs)
    