from environs import Env
from rest_framework import serializers

from shoplus import Shoplus, ShoplusError, COUNTRY_CODES

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
        username, password = load_credentials("credentials.env")
        shoplus = Shoplus(username, password)
        shoplus.login()

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


def load_credentials(env_file):
    env = Env()
    env.read_env(env_file)

    username = env.str("SHOPLUS_USERNAME")
    password = env.str("SHOPLUS_PASSWORD")

    return username, password
