from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import stripe


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(
            username=username.lower(),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, db_index=True, unique=True)
    stripe_id = models.CharField(max_length=32, blank=True)
    last_login = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.set_stripe_id()
        return super().save(*args, **kwargs)

    def set_stripe_id(self):
        if not self.stripe_id:
            customer = stripe.Customer.create(name=self.username)
            self.stripe_id = customer.id

    def __str__(self):
        return str(self.username)
