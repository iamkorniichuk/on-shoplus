from rest_framework import serializers
import stripe

from subscriptions.models import Subscription


class PaymentMethodSerializer(serializers.Serializer):
    payment_method = serializers.CharField()

    def validate_payment_method(self, value):
        return stripe.PaymentMethod.retrieve(value).id


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

    is_active = serializers.BooleanField(read_only=True)
    is_canceled = serializers.BooleanField(read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)

        response = stripe.Subscription.retrieve(instance.stripe_id)

        result["is_active"] = response["status"] == "active"
        result["is_canceled"] = response["cancel_at_period_end"]

        return result
