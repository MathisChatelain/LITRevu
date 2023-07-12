from django.shortcuts import render, redirect

from . import forms
from django.contrib.auth import (
    login,
    authenticate,
    logout,
)
from django.contrib.auth.models import User


def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
        message = "Identifiants invalides."
    return render(
        request, "authentication/login.html", context={"form": form, "message": message}
    )


def signup(request):
    form = forms.SignupForm()
    message = ""
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # We authenticate the user to log him in if the account already exists
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                # We create the user if it does not exist
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                )
                user.save()
                login(request, user)
                return redirect("home")
    return render(
        request,
        "authentication/signup.html",
        context={"form": form, "message": message},
    )


def logout_user(request):
    logout(request)
    return redirect("login")
