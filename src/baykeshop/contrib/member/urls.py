from django.urls import path

from . import views

app_name = 'member'

urlpatterns = [
    path('login/', views.BaykeShopUserLoginView.as_view(), name='login'),
    path('logout/', views.BaykeShopUserLogoutView.as_view(), name='logout'),
    path('register/', views.BaykeShopUserRegisterView.as_view(), name='register'),
    path('profile/', views.BaykeShopUserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', views.BaykeShopUserProfileUpdateView.as_view(), name='profile-update'),
    path('address/', views.BaykeShopUserAddressListView.as_view(), name='address-list'),
    path('password/', views.BaykeShopUserPasswordView.as_view(), name='password'),
    path('address/create/', views.BaykeShopUserAddressCreateView.as_view(), name='address-create'),
    path('address/<int:pk>/update/', views.BaykeShopUserAddressUpdateView.as_view(), name='address-update'),
    path('address/<int:pk>/delete/', views.BaykeShopUserAddressDeleteView.as_view(), name='address-delete'),
    path('orders/', views.BaykeShopOrdersListView.as_view(), name='orders-list'),
    path('orders/<slug:order_sn>/', views.BaykeShopOrdersDetailView.as_view(), name='orders-detail'),
    # 订单相关操作
    path('orders/<slug:order_sn>/comment/', views.CommentActionView.as_view(), name='orders-comment'),
    path('orders/<slug:order_sn>/receipt/', views.OrderStatusActionView.as_view(), name='orders-receipt'),
]