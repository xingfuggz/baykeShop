from django.urls import path, include

app_name = "baykeshop"

urlpatterns = [
    path("", include("baykeshop.public.urls")),
    path('goods/', include('baykeshop.module.product.urls'), name='goods'),
    path('cart/', include('baykeshop.module.cart.urls'), name='cart'),
    path('user/', include('baykeshop.module.user.urls'), name='user'),
    path('payment/', include('baykeshop.module.payment.urls'), name='payment'),
    path('order/', include('baykeshop.module.order.urls'), name='order'),
]
