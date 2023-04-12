from django.urls import path
from baykeshop.module.user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]

router.register('address', views.BaykeShopAddressViewset, basename="address")

urlpatterns += router.urls