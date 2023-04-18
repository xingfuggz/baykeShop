from rest_framework.routers import DefaultRouter

from baykeshop.module.order import views

router = DefaultRouter()

router.register('', views.BaykeOrderInfoViewset, basename="orders")

router.register('confirm', views.BaykeOrderGoodsViewset, basename="confirm")

urlpatterns = router.urls