from django.urls import path
from baykeshop.public import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path("upload/tinymce/", views.TinymceUploadImg.as_view(), name="upload_tinymce"),
]