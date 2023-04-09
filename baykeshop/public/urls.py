from django.urls import path, include
from baykeshop.public import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('goods/', include('baykeshop.module.product.urls'), name='goods'),
]