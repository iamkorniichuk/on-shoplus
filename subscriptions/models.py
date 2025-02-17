from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Subscription(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name="subscription")
    stripe_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.stripe_id


class InvoicePaidEvent(models.Model):
    stripe_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.stripe_id
