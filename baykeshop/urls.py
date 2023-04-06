from django.urls import path, include


urlpatterns = [
    path("", include("baykeshop.public.urls"))
]
