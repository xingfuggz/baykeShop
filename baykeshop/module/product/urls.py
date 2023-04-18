from django.urls import path

from rest_framework.routers import DefaultRouter

from baykeshop.module.product import views


router = DefaultRouter()

router.register('', views.BaykeGoodsViewSet, basename="goods")
router.register('spu', views.BaykeGoodsDetailViewSet, basename="spu")

urlpatterns = router.urls
urlpatterns += [
    path('cache/', views.BaykeCacheGoodsAPIview.as_view(), name='cache'),
]
