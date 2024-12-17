from django.urls import path

from . import views

app_name = "member"

urlpatterns = [
    # 登录
    path("login/", views.BaykeShopUserLoginView.as_view(), name="login"),
    # 登出
    path("logout/", views.BaykeShopUserLogoutView.as_view(), name="logout"),
    # 注册
    path("register/", views.BaykeShopUserRegisterView.as_view(), name="register"),
    # 个人中心
    path("profile/", views.BaykeShopUserProfileView.as_view(), name="profile"),
    # 修改个人信息
    path(
        "profile/<int:pk>/update/",
        views.BaykeShopUserProfileUpdateView.as_view(),
        name="profile-update",
    ),
    # 个人中心修改密码
    path(
        "password/", 
        views.BaykeShopUserPasswordView.as_view(), 
        name="password"
    ),
    # 地址列表
    path(
        "address/", 
        views.BaykeShopUserAddressListView.as_view(), 
        name="address-list"
    ),
    # 添加地址
    path(
        "address/create/",
        views.BaykeShopUserAddressCreateView.as_view(),
        name="address-create",
    ),
    # 修改地址
    path(
        "address/<int:pk>/update/",
        views.BaykeShopUserAddressUpdateView.as_view(),
        name="address-update",
    ),
    # 删除地址
    path(
        "address/<int:pk>/delete/",
        views.BaykeShopUserAddressDeleteView.as_view(),
        name="address-delete",
    ),
    # 订单列表
    path(
        "orders/", 
        views.BaykeShopOrdersListView.as_view(), 
        name="orders-list"
    ),
    # 订单详情
    path(
        "orders/<slug:order_sn>/",
        views.BaykeShopOrdersDetailView.as_view(),
        name="orders-detail",
    ),
    # 订单相关操作，订单评论
    path(
        "orders/<slug:order_sn>/comment/",
        views.CommentActionView.as_view(),
        name="orders-comment",
    ),
    # 确认收货
    path(
        "orders/<slug:order_sn>/receipt/",
        views.OrderStatusActionView.as_view(),
        name="orders-receipt",
    ),
    ############### 忘记密码相关操作 START ################
    # 忘记密码
    path(
        "password/reset/",
        views.BaykePasswordResetView.as_view(),
        name="password_reset",
    ),
    # 重置密码
    path(
        "password/reset/done/",
        views.BaykePasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        views.BaykePasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # 重置密码完成
    path(
        "password/reset/complete/",
        views.BaykePasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    ################ 忘记密码相关操作 END ################
]
