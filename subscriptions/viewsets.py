from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
import stripe

from subscriptions.models import Subscription

from .serializers import SubscriptionSerializer


PRICE_STRIPE_ID = "price_1QZewDRx6js27MSIw6PWkuwA"


class SubscriptionViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = SubscriptionSerializer
    model = Subscription

    def get_object(self):
        user = self.request.user
        return user.subscription

    def create(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            stripe.Subscription.resume(obj.stripe_id)
            data = {"stripe_id": obj.stripe_id}
        else:
            customer = request.user.stripe_id
            payment_method = request.data.get("payment_method")
            subscription = stripe.Subscription.create(
                customer=customer,
                default_payment_method=payment_method,
                items=[{"price": PRICE_STRIPE_ID}],
            )
            data = {
                "stripe_id": subscription.id,
            }

        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        serializer.save(user=self.request.user)
        return Response(
            serializer.to_representation(),
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.to_representation())

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            stripe.Subscription.cancel(obj.stripe_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
