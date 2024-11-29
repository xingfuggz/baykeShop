from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('category/list/', views.BaykeGalleryCategoryListView.as_view(), name='category-list'),
    path('category/<int:category_id>/detail/', views.BaykeGalleryCategoryDetailView.as_view(), name='category-detail'),
    path('gallery/list/', views.BaykeGalleryListView.as_view(), name='gallery-list'),
]