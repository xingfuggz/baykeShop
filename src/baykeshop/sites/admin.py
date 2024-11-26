from django.contrib import admin
from baykeshop.forms import ModelForm

class TabularInline(admin.TabularInline):
    '''Tabular Inline View for '''
    pass


class StackedInline(admin.StackedInline):
    '''Stacked Inline View for '''
    pass


class ModelAdmin(admin.ModelAdmin):
    """自定义ModelAdmin"""
    form = ModelForm

