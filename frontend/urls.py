from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import login_view, signup_view, SearchShopViewSet


router = SimpleRouter()
router.register("shops", SearchShopViewSet, "shops")


app_name = "frontend"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
] + router.urls
