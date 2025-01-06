from rest_framework.permissions import BasePermission
import stripe


class HasSubscription(BasePermission):
    error_message = "You need to be subscribed."

    def has_object_permission(self, request, view, obj):
        obj = request.user.subscription
        if not obj:
            return False

        subscription = stripe.Subscription.retrieve(obj.stripe_id)
        return subscription.status == "active"
