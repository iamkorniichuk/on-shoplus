from rest_framework import serializers

from commons.shoplus import Shoplus


COUNTRY_CHOICES = list(Shoplus.COUNTRIES_MAP.items())


class SearchShopSerializer(serializers.Serializer):
    query = serializers.CharField()
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
