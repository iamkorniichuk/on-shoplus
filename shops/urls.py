from rest_framework.routers import SimpleRouter

from .viewsets import SearchShopViewSet


app_name = "shops"

router = SimpleRouter()
router.register("search", SearchShopViewSet, "search")

urlpatterns = router.urls
