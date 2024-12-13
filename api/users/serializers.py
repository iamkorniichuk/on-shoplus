from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as LoginSerializer


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "username": {"write_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
