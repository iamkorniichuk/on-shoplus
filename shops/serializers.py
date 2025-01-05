from environs import Env
from rest_framework import serializers
from playwright.sync_api import sync_playwright

from shoplus import Shoplus, COUNTRY_CODES

from .models import SearchShopHistory


COUNTRY_CHOICES = list(COUNTRY_CODES.items())


class SearchShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchShopHistory
        fields = "__all__"
        read_only_fields = ("result", "created_at")
        extra_kwargs = {
            "user": {"write_only": True},
        }

    query = serializers.ListField(child=serializers.CharField(), write_only=True)
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES, write_only=True)

    def create(self, validated_data):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()

            shoplus = Shoplus(context)

            username, password = load_credentials("credentials.env")
            shoplus.login(username, password)

            query = validated_data.pop("query")
            country = validated_data.pop("country")

            result = {}
            for name in query:
                result[name] = shoplus.search_shop(
                    name,
                    country=country,
                )
            validated_data["result"] = result

        return super().create(validated_data)


def load_credentials(env_file):
    env = Env()
    env.read_env(env_file)

    username = env.str("SHOPLUS_USERNAME")
    password = env.str("SHOPLUS_PASSWORD")

    return username, password
