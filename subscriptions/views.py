from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

import stripe, stripe.error

from .models import InvoicePaidEvent


User = get_user_model()


@require_POST
@csrf_exempt
def invoice_paid_webhook(request):
    event = None

    payload = request.body
    signature = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = settings.STRIPE_PAID_WEBHOOK_ENDPOINT_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, signature, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

    if not event or event["type"] != "invoice.payment_succeeded":
        return HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)

    invoice = event["data"]["object"]
    event_id = event["id"]

    obj, created = InvoicePaidEvent.objects.get_or_create(stripe_id=event_id)
    if not created:
        return HttpResponse(status=status.HTTP_429_TOO_MANY_REQUESTS)

    customer_id = invoice["customer"]
    user = get_object_or_404(User, stripe_id=customer_id)

    referrer = user.referrer
    if not referrer or not referrer.account_stripe_id:
        return HttpResponse(status=status.HTTP_200_OK)

    amount = invoice.amount_paid // 10
    currency = invoice.currency
    account_id = referrer.account_stripe_id
    stripe.Transfer.create(
        amount=amount,
        currency=currency,
        destination=account_id,
    )
    return HttpResponse(status=status.HTTP_201_CREATED)
