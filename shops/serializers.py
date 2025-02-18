from django.conf import settings
from rest_framework import serializers

from shoplus import Shoplus, COUNTRY_CODES
from shoplus.errors import ShoplusError, AuthorizationError

from .models import SearchShopHistory


COUNTRY_CHOICES = list(COUNTRY_CODES.items())


class SearchShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchShopHistory
        fields = "__all__"
        read_only_fields = ("result", "created_at", "user")

    query = serializers.ListField(child=serializers.CharField(), write_only=True)
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES, write_only=True)

    def validate(self, attrs):
        try:
            self.shoplus = self.login_shoplus()
            return attrs
        except AuthorizationError:
            return serializers.ValidationError("Server's credentials are invalid")

    def login_shoplus(self):
        public_key = settings.SHOPLUS_PUBLIC_KEY
        shoplus = Shoplus(public_key)

        username = settings.SHOPLUS_USERNAME
        password = settings.SHOPLUS_PASSWORD
        shoplus.login(username, password)

        return shoplus

    def create(self, validated_data):
        query = validated_data.pop("query")
        country = validated_data.pop("country")

        result = {}
        for name in query:
            try:
                result[name] = self.shoplus.search_shop(
                    name,
                    country=country,
                )
            except AuthorizationError:
                self.shoplus = self.login_shoplus()
            except ShoplusError:
                break

        validated_data["result"] = {
            key: result[key]
            for key in sorted(result.keys(), key=lambda k: not result[k])
        }

        return super().create(validated_data)
