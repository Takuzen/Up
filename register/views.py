from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model

from app.forms import SignUpForm
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from .forms import LoginForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.models import Item


# Create your views here.
def register(response):
    model = get_user_model()
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(response, f'{username}さんのアカウントが登録されました!')
        return redirect("/")
    else:
        form = SignUpForm()
    return render(response, "register/register.html", {"form": form})

@login_required
def profile(request):
    user_posts = Item.objects.filter(created_by_id = request.user.id)
    return render(request, 'register/profile.html', {'user_posts': user_posts})


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'register/login.html'
