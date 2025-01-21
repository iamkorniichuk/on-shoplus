from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response

import stripe, stripe.error


User = get_user_model()


class InvoicePaidWebhook(views.APIView):
    def post(self, request):
        event = None

        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        signature = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(
                request.data, signature, endpoint_secret
            )
        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if event and event["type"] == "invoice.paid":
            invoice = event["data"]["object"]
            customer_id = invoice.customer
            user = get_object_or_404(User, stripe_id=customer_id)

            referrer = user.referrer
            if not referrer or not referrer.account_stripe_id:
                return Response(status=status.HTTP_200_OK)

            amount = invoice.amount_paid // 10
            currency = invoice.currency
            account_id = referrer.account_stripe_id
            stripe.Transfer.create(
                amount=amount,
                currency=currency,
                destination=account_id,
            )
            return Response(status=status.HTTP_201_CREATED)
