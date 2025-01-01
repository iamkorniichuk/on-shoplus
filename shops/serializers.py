from rest_framework import serializers

from shoplus import COUNTRY_CODES


COUNTRY_CHOICES = list(COUNTRY_CODES.items())


class SearchShopSerializer(serializers.Serializer):
    query = serializers.CharField()
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
