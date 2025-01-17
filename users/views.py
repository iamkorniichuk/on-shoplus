from django.contrib.auth import login
from django.conf import settings
from rest_framework import permissions, mixins, viewsets, status
from rest_framework.response import Response

from knox.views import (
    LoginView as KnoxLoginView,
    LogoutView,
    LogoutAllView,
)
from knox.auth import TokenAuthentication
import stripe

from .serializers import LoginSerializer, SignupSerializer, StripeUrlsSerializer
from .models import User


class AccountViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = StripeUrlsSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        stripe_id = self.request.user.account_stripe_id
        if not stripe_id:
            return None
        return stripe.Account.retrieve(stripe_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = self.get_object()
        if account:
            disabled_reason = account.requirements.disabled_reason
            if (
                disabled_reason == None
                or disabled_reason == "requirements.pending_verification"
            ):
                return Response(
                    "Account has already been created",
                    status=status.HTTP_409_CONFLICT,
                )
        else:
            url = (
                "https://some-example.com/"
                if settings.DEBUG
                else request.build_absolute_uri("/")
            )
            account = stripe.Account.create(
                type="standard",
                business_type="individual",
                business_profile={
                    "mcc": 5969,
                    "name": "Affiliate program",
                    "product_description": "I receive affiliate fees from marketing platforms",
                    "url": url,
                },
            )
            user = self.request.user
            user.account_stripe_id = account.id
            user.save()

        link = stripe.AccountLink.create(
            account=account.id,
            type="account_onboarding",
            **serializer.data,
        )
        return Response({"url": link.url}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = self.get_object()
        if account:
            link = stripe.AccountLink.create(
                account=account.id,
                type="account_update",
                **serializer.data,
            )
            return Response({"url": link.url}, status=status.HTTP_200_OK)
        else:
            return Response(
                "No account has been found",
                status=status.HTTP_404_NOT_FOUND,
            )


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        user = self.get_validated_user(request.data)

        login(request, user)
        return super().post(request, format=format)

    def get_validated_user(self, data):
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return user


class SignupView(LoginView):
    permission_classes = (permissions.AllowAny,)

    def get_validated_user(self, data):
        serializer = SignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = serializer.create(validated_data)
        return user
