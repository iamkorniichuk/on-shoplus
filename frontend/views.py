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

def history_view(request, pk):
    obj = SearchShopHistory.objects.get(pk=pk)
    context = {
        "title": "Shops",
        "url": obj.get_absolute_url(),
    }
    return render(request, "shops/history.html", context=context)

def checkout_view(request):
    context = {
        "title": "Checkout",
    }
    return render(request, "subscriptions/checkout.html", context=context)

def subscription_info_view(request):
    context = {
        "title": "Subscription Info",
    }
    return render(request, "subscriptions/info.html", context=context)