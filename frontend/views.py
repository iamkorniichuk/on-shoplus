from django.shortcuts import render
from django.urls import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import mixins, viewsets

from shops.models import SearchShopHistory


def login_view(request):
    context = {
        "title": "Login",
        "url": reverse("users:login"),
    }
    return render(request, "users/auth_form.html", context=context)


def signup_view(request):
    context = {
        "title": "Sign Up",
        "url": reverse("users:signup"),
    }
    return render(request, "users/auth_form.html", context=context)


class SearchShopViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        queryset = SearchShopHistory.objects
        if self.action != "retrieve":
            user = self.request.user
            queryset = queryset.filter(user=user)
        return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
            "title": "Shops",
            "url": obj.get_absolute_url(),
        }
        return render(request, "shops/detail.html", context=context)
