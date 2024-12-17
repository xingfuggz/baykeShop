from .auth import (
    BaykeShopUserLoginView,
    BaykeShopUserLogoutView,
    BaykeShopUserRegisterView,
    BaykePasswordResetView,
    BaykePasswordResetDoneView,
    BaykePasswordResetConfirmView,
    BaykePasswordResetCompleteView,
)
from .profile import (
    BaykeShopUserProfileView,
    BaykeShopUserAddressListView,
    BaykeShopUserPasswordView,
    BaykeShopUserAddressCreateView,
    BaykeShopUserAddressUpdateView,
    BaykeShopUserAddressDeleteView,
    BaykeShopUserProfileUpdateView,
)
from .orders import BaykeShopOrdersListView, BaykeShopOrdersDetailView
from .actions import OrderStatusActionView, CommentActionView
