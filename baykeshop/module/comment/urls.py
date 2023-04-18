from rest_framework.routers import DefaultRouter

from baykeshop.module.comment import views

router = DefaultRouter()

router.register('', views.BaykeOrderInfoCommentsViewset, basename='comment')

urlpatterns = router.urls