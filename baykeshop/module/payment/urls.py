from django.urls import path
from baykeshop.module.payment import views


urlpatterns = [
    path('confirm/', views.ConfirmOrderAPIView.as_view(), name='confirm'),
]