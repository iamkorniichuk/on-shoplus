from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse

from shops.models import SearchShopHistory


User = get_user_model()


def login_view(request):
    context = {
        "title": "Login",
        "url": reverse("users:login"),
        "referrer": None,
    }
    return render(request, "users/auth_form.html", context=context)


def signup_view(request):
    referrer = request.GET.get("referrer", None)
    user = User.objects.filter(username=referrer).first()
    if user:
        user = user.pk

    context = {
        "title": "Sign Up",
        "url": reverse("users:signup"),
        "referrer": user,
    }
    return render(request, "users/auth_form.html", context=context)


def logout_view(request):
    context = {
        "title": "Log Out",
        "url": reverse("users:logout"),
    }
    return render(request, "users/logout.html", context=context)


def logout_all_view(request):
    context = {
        "title": "Log Out All",
        "url": reverse("users:logout-all"),
    }
    return render(request, "users/logout.html", context=context)


def history_view(request, pk):
    obj = SearchShopHistory.objects.get(pk=pk)
    context = {
        "title": "Shops",
        "url": obj.get_absolute_url(),
    }
    return render(request, "shops/history.html", context=context)


def history_list_view(request):
    current_user = request.user
    queryset = SearchShopHistory.objects.filter(user=current_user).all()
    context = {
        "title": "Shops",
        "queryset": queryset,
    }
    return render(request, "shops/history_list.html", context=context)


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


def referral_register_view(request):
    context = {
        "title": "Register Stripe",
    }
    return render(request, "referrals/register.html", context=context)


def referral_success_view(request):
    context = {
        "title": "Success",
    }
    return render(request, "referrals/success.html", context=context)
