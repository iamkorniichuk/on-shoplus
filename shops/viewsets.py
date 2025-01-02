from rest_framework import viewsets, mixins

from commons.viewsets import OverrideCreateRequestData

from .serializers import SearchShopSerializer
from .models import SearchShopHistory


class SearchShopViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    OverrideCreateRequestData,
):
    serializer_class = SearchShopSerializer

    def get_queryset(self):
        queryset = SearchShopHistory.objects
        if self.action != "retrieve":
            user = self.request.user
            queryset = queryset.filter(user=user)
        return queryset.all()

    def get_overriding_data(self):
        return {"user": self.request.user}
