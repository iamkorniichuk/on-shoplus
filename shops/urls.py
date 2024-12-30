from django.urls import path

from .views import search_shop


app_name = "shops"

urlpatterns = [
    path("", search_shop, name="search"),
]
