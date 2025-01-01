from django.shortcuts import render

from shoplus import COUNTRY_CODES


def login_view(request):
    return render(request, "users/login.html")


def shops_view(request):
    context = {
        "countries": COUNTRY_CODES,
    }
    return render(request, "shops/shops.html", context=context)
