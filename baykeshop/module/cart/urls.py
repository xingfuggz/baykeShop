from django.urls import path

from rest_framework.routers import DefaultRouter

from baykeshop.module.cart import views


router = DefaultRouter()

router.register('', views.BaykeshopingCartViewSet, basename="carts")

urlpatterns = router.urls