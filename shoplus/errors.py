class ShoplusError(Exception):
    pass


class AuthorizationError(ShoplusError):
    pass


class SubscriptionError(ShoplusError):
    pass


class QuotaError(ShoplusError):
    pass
