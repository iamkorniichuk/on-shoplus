from django.shortcuts import render
from django.urls import reverse


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
