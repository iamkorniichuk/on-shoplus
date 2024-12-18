from django.urls import path, include


def api_path(route, app_name, url_path=None):
    app_name = f"api.{app_name}"

    if not url_path:
        url_path = f"{app_name}.urls"

    return path(route, include((url_path, app_name)))


urlpatterns = [
    api_path("auth/", "users"),
    api_path("shops/", "shops"),
]
