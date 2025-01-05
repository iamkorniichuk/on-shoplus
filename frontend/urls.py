from django.urls import path

from .views import login_view, signup_view, history_view

app_name = "frontend"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("shops/<int:pk>/", history_view, name="history"),
]
