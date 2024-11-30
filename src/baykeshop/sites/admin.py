from django.contrib import admin
from baykeshop.forms import ModelForm


class TabularInline(admin.TabularInline):
    '''Tabular Inline View for '''
    form = ModelForm


class StackedInline(admin.StackedInline):
    '''Stacked Inline View for '''
    form = ModelForm


class ModelAdmin(admin.ModelAdmin):
    """自定义ModelAdmin"""
    form = ModelForm

    # class Media:
    #     css = {
    #         "all": (
    #             "/static/baykeshop/css/bayke.css",
    #             "/static/baykeshop/css/materialdesignicons.min.css",
    #         )
    #     }
    #     js = (
    #         '/static/baykeshop/js/vue.global.js',
    #     )



