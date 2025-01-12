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
        obj = self.get_object()
        user = self.request.user

        if obj:
            stripe.Subscription.resume(obj.stripe_id)
            stripe_id = obj.stripe_id
        else:
            customer = user.stripe_id
            payment_method = request.data.get("payment_method")
            stripe.PaymentMethod.attach(
                payment_method,
                customer=customer,
            )
            subscription = stripe.Subscription.create(
                customer=customer,
                default_payment_method=payment_method,
                items=[{"price": PRICE_STRIPE_ID}],
            )
            stripe_id = subscription.id

        data = {"stripe_id": stripe_id, "user": user.pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        serializer.save()
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
