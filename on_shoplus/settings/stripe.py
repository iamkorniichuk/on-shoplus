import stripe

from .base import env
from .security import DEBUG


if DEBUG:
    stripe.api_key = env.str("STRIPE_TEST_PRIVATE_KEY")
else:
    stripe.api_key = env.str("STRIPE_LIVE_PRIVATE_KEY")
