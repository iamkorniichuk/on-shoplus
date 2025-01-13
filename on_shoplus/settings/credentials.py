import stripe
from environs import Env

from .security import DEBUG


env = Env()
env.read_env("credentials.env")


if DEBUG:
    stripe.api_key = env.str("STRIPE_TEST_PRIVATE_KEY")
    STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_TEST_PUBLISHABLE_KEY")
else:
    stripe.api_key = env.str("STRIPE_LIVE_PRIVATE_KEY")
    STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_LIVE_PUBLISHABLE_KEY")


SHOPLUS_USERNAME = env.str("SHOPLUS_USERNAME")
SHOPLUS_PASSWORD = env.str("SHOPLUS_PASSWORD")
SHOPLUS_PUBLIC_KEY = env.str("SHOPLUS_PUBLIC_KEY")
