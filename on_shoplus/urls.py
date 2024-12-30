from django.urls import path, include


api_urls = [
    path("auth/", include("users.urls")),
    path("shops/", include("shops.urls")),
]

urlpatterns = [
    path("api/", include(api_urls)),
    path("", include("frontend.urls")),
]
