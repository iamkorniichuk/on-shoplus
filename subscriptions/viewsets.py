from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from knox.auth import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
import stripe

from subscriptions.models import Subscription

from .serializers import SubscriptionSerializer, PaymentMethodSerializer


PRICE_STRIPE_ID = "price_1QgSKgCD4T1ii2MY91Rm3Dkq"


class SubscriptionViewSet(
    mixins.ListModelMixin,
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

    @swagger_auto_schema(request_body=PaymentMethodSerializer)
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PaymentMethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_method = serializer.data["payment_method"]

        if user.stripe_id:
            customer = stripe.Customer.retrieve(user.stripe_id)
            customer.update(
                {
                    "payment_method": payment_method,
                    "invoice_settings": {"default_payment_method": payment_method},
                }
            )
        else:
            customer = stripe.Customer.create(
                name=user.username,
                payment_method=payment_method,
                invoice_settings={"default_payment_method": payment_method},
            )
            user.stripe_id = customer.id
            user.save()

        obj = Subscription.objects.filter(user=user).first()
        if obj:
            subscription = stripe.Subscription.retrieve(obj.stripe_id)
            if not subscription:
                obj.delete()
                obj = None

        if not obj:
            subscription = stripe.Subscription.create(
                customer=customer,
                items=[{"price": PRICE_STRIPE_ID}],
            )
            obj = Subscription.objects.create(user=user, stripe_id=subscription.id)

        serializer = self.get_serializer(obj)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        user = request.user
        obj = get_object_or_404(Subscription, user=user)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        obj = get_object_or_404(Subscription, user=user)
        stripe.Subscription.modify(
            obj.stripe_id,
            cancel_at_period_end=True,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
