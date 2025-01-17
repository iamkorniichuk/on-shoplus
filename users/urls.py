from django.urls import path
from rest_framework.routers import SimpleRouter, Route

from .views import SignupView, LoginView, LogoutView, LogoutAllView, AccountViewSet


class AccountRouter(SimpleRouter):
    routes = [
        Route(
            url="{prefix}{trailing_slash}",
            mapping={
                "post": "create",
                "put": "update",
                "patch": "update",
            },
            name="{basename}",
            detail=False,
            initkwargs={"suffix": "List"},
        )
    ]


router = AccountRouter()
router.register("account", AccountViewSet, "account")


app_name = "users"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout-all/", LogoutAllView.as_view(), name="logout-all"),
] + router.urls
