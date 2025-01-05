from django.urls import path

from .views import SearchShopHistoryView, SearchShopView


app_name = "shops"


urlpatterns = [
    path("", SearchShopView.as_view(), name="search"),
    path("<int:pk>", SearchShopHistoryView.as_view(), name="history"),
]
