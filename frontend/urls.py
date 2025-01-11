from django.urls import path

from .views import login_view, signup_view, history_view, checkout_view, subscription_info_view

app_name = "frontend"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("shops/<int:pk>/", history_view, name="history"),
    path("subscriptions/checkout/", checkout_view, name="checkout"),
    path("subscriptions/info/", subscription_info_view, name="checkout"),
]
