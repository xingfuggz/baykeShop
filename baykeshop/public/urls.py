from django.urls import path
from baykeshop.public import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
]