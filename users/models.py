from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


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
    stripe_id = models.CharField(max_length=64, blank=True, null=True)
    referrer = models.ForeignKey(
        "users.User",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
    )
    account_stripe_id = models.CharField(max_length=64, blank=True, null=True)
    last_login = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.username)
