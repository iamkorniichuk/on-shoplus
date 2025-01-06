from .routers import SubscriptionRouter
from .viewsets import SubscriptionViewSet


router = SubscriptionRouter()
router.register("", SubscriptionViewSet, "")

urlpatterns = router.urls
