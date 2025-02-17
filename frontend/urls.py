from django.urls import path

from .views import (
    login_view,
    signup_view,
    logout_view,
    logout_all_view,
    history_view,
    history_list_view,
    checkout_view,
    subscription_info_view,
    referral_register_view,
    referral_success_view,
)

app_name = "frontend"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("logout-all/", logout_all_view, name="logout-all"),
    path("shops/<int:pk>/", history_view, name="history"),
    path("shops/", history_list_view, name="history-list"),
    path("subscription/", checkout_view, name="subscribe"),
    path("subscription/info/", subscription_info_view, name="subscription"),
    path("referral/register/", referral_register_view, name="referral-register"),
    path("referral/success/", referral_success_view, name="referral-success"),
]
