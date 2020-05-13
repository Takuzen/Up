from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model

from app.forms import SignUpForm
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from .forms import LoginForm


# Create your views here.
def register(response):
    model = get_user_model()
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
            print("saved")
        return redirect("/")
    else:
        form = SignUpForm()
    return render(response, "register/register.html", {"form": form})


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'register/login.html'