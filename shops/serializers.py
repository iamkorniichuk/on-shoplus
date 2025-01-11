from django.conf import settings
from rest_framework import serializers

from shoplus.errors import ShoplusError
from shoplus import Shoplus, COUNTRY_CODES

from .models import SearchShopHistory


COUNTRY_CHOICES = list(COUNTRY_CODES.items())


class SearchShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchShopHistory
        fields = "__all__"
        read_only_fields = ("result", "created_at")
        extra_kwargs = {
            "user": {"write_only": True, "required": False},
        }

    query = serializers.ListField(child=serializers.CharField(), write_only=True)
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES, write_only=True)

    def create(self, validated_data):
        public_key = settings.SHOPLUS_PUBLIC_KEY
        shoplus = Shoplus(public_key)

        username = settings.SHOPLUS_USERNAME
        password = settings.SHOPLUS_PASSWORD
        shoplus.login(username, password)

        query = validated_data.pop("query")
        country = validated_data.pop("country")

        result = {}
        for name in query:
            try:
                result[name] = shoplus.search_shop(
                    name,
                    country=country,
                )
            except ShoplusError:
                pass

        validated_data["result"] = {
            key: result[key]
            for key in sorted(result.keys(), key=lambda k: not result[k])
        }

        return super().create(validated_data)
