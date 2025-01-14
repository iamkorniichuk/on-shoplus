from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


api_urls = [
    path("user/", include("users.urls")),
    path("shops/", include("shops.urls")),
    path("subscription/", include("subscriptions.urls")),
]

schema_view = get_schema_view(
    openapi.Info(title="On Shoplus API", default_version="v.0.1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=api_urls,
)

urlpatterns = [
    path("api/schema/", schema_view.with_ui("swagger", cache_timeout=0), name="schema"),
    path("api/", include(api_urls)),
    path("", include("frontend.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
