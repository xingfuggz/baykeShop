from django.urls import path, include

app_name = "baykeshop"

urlpatterns = [
    path("", include("baykeshop.public.urls"))
]
