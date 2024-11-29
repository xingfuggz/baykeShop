from django.contrib import admin

# Register your models here.
from baykeshop.sites import admin as bayke_admin
from .models import *


class BaykeGalleryInline(bayke_admin.TabularInline):
    extra = 0
    model = BaykeGallery


@admin.register(BaykeGalleryCategory)
class BaykeGalleryCategoryAdmin(bayke_admin.ModelAdmin):
    list_display = ('name', 'created_time', 'updated_time')
    list_filter = ('name', 'created_time', 'updated_time')
    search_fields = ('name',)
    inlines = (BaykeGalleryInline,)