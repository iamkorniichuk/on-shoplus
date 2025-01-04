from django.urls import path

from .views import login_view, signup_view, shops_list_view


app_name = "frontend"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("shops/search/<int:id>", shops_list_view, name="shops-list"),
]
