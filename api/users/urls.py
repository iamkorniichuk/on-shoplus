from django.urls import path

from .views import SignupApiView, LoginApiView, LogoutApiView, LogoutAllApiView


urlpatterns = [
    path("signup/", SignupApiView.as_view(), name="signup"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("logout-all/", LogoutAllApiView.as_view(), name="logout-all"),
]
