from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register("", views.BaykeArticleViewset, basename="article")

urlpatterns = router.urls