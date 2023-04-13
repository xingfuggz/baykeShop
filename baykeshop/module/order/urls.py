from rest_framework.routers import DefaultRouter

from baykeshop.module.order import views

router = DefaultRouter()

router.register('', views.BaykeOrderInfoViewset, basename="orders")

urlpatterns = router.urls