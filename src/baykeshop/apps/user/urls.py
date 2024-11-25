from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.BaykeShopLoginView.as_view(), name='login'),
    path('logout/', views.BaykeShopLogoutView.as_view(), name='logout'),
    path('register/', views.BaykeShopRegisterView.as_view(), name='register'),
    path('account/', views.BaykeShopAccountView.as_view(), name='account'),
    path('change-password/', views.BaykeShopPasswordChangeView.as_view(), name='change-password'),
    path('change-profile/', views.BaykeShopUserProfileUpdateView.as_view(), name='change-profile'),
    path('address/', views.BaykeShopUserAddressView.as_view(), name='address-list'),
    path('address/create/', views.BaykeShopUserAddressCreateView.as_view(), name='address-create'),
    path('address/<int:pk>/', views.BaykeShopUserAddressUpdateView.as_view(), name='address-update'),
    path('address/delete/<int:pk>/', views.UserAddressDeleteView.as_view(), name='address-delete')
    # path("accounts/", include("django.contrib.auth.urls")),
]