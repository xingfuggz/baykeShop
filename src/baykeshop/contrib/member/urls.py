from django.urls import path

from . import views

app_name = 'member'

urlpatterns = [
    path('login/', views.BaykeShopUserLoginView.as_view(), name='login'),
]