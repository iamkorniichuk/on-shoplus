from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


api_urls = [
    path("", include("users.urls")),
    path("shops/", include("shops.urls")),
    path("subscriptions/", include("subscriptions.urls")),
]

urlpatterns = [
    path("api/", include(api_urls)),
    path("", include("frontend.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)