from django.urls import path

from .routers import SubscriptionRouter
from .viewsets import SubscriptionViewSet
from .views import InvoicePaidWebhook


router = SubscriptionRouter()
router.register("", SubscriptionViewSet, "")

urlpatterns = [
    path("paid-webhook/", InvoicePaidWebhook.as_view(), name="invoice-paid"),
] + router.urls
