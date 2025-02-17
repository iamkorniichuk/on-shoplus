from django.urls import path

from .routers import SubscriptionRouter
from .viewsets import SubscriptionViewSet
from .views import invoice_paid_webhook


router = SubscriptionRouter()
router.register("", SubscriptionViewSet, "")

urlpatterns = [
    path("paid-webhook/", invoice_paid_webhook, name="invoice-paid"),
] + router.urls
