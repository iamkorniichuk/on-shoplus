from rest_framework import status, mixins, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from knox.auth import TokenAuthentication
import stripe

from subscriptions.models import Subscription

from .serializers import SubscriptionSerializer


PRICE_STRIPE_ID = "price_1QgSKgCD4T1ii2MY91Rm3Dkq"


class SubscriptionViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        user = self.request.user
        subscription = Subscription.objects.filter(user=user).first()
        return subscription

    def create(self, request, *args, **kwargs):
        user = self.request.user
        stripe_id = request.data.get("payment_method")
        payment_method = stripe.PaymentMethod.retrieve(stripe_id)

        customer = stripe.Customer.create(
            name=user.username,
            payment_method=payment_method,
            invoice_settings={"default_payment_method": payment_method},
        )
        subscription = stripe.Subscription.create(
            customer=customer,
            items=[{"price": PRICE_STRIPE_ID}],
        )

        user.stripe_id = customer.id
        user.save()

        instance = Subscription.objects.create(user=user, stripe_id=subscription.id)
        serializer = self.get_serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj:
            stripe.Subscription.cancel(obj.stripe_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
