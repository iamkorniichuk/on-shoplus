from rest_framework import generics, permissions
from knox.auth import TokenAuthentication

from subscriptions.permissions import HasSubscription

from .serializers import SearchShopSerializer
from .models import SearchShopHistory


class SearchShopView(generics.CreateAPIView):
    serializer_class = SearchShopSerializer
    queryset = SearchShopHistory.objects.all()
    permission_classes = [permissions.IsAuthenticated, HasSubscription]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchShopHistoryView(generics.RetrieveAPIView):
    serializer_class = SearchShopSerializer
    queryset = SearchShopHistory.objects.all()
