from django.urls import path

from .views import *


app_name = "frontend"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("shops/", shops_view, name="shops"),
]
