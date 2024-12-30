from django.contrib.auth import login

from rest_framework.permissions import AllowAny
from knox.views import (
    LoginView as KnoxLoginView,
    LogoutView,
    LogoutAllView,
)

from .serializers import LoginSerializer, SignupSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    def get_validated_user(self, data):
        serializer = SignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = serializer.create(validated_data)
        return user
