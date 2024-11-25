from django.urls import path

from . import views

app_name = 'core'


urlpatterns = [
    path(
        'upload/image/', 
        views.UploadImageView.as_view(), 
        name='upload-image'
    ),
]