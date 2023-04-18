from django.urls import path
from rest_framework.routers import DefaultRouter

from . import token
from baykeshop.module.user import views


router = DefaultRouter()

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    
    path("token/", token.BaykeTokenObtainPairView.as_view(), name="token"),
]

router.register('address', views.BaykeShopAddressViewset, basename="address")

router.register('menmber', views.UserMenmberViewset, basename='menmber')

urlpatterns += router.urls