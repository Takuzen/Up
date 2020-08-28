from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from ..app.forms import SignUpForm
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from .forms import LoginForm, UpdateProfile

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..app.models import Item


# Create your views here.
def register(response):
    model = get_user_model()
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(response, f'{username}さんのアカウントが登録されました!')
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            login(response, new_user)
        return redirect("/")
    else:
        form = SignUpForm()
    return render(response, "register/register.html", {"form": form})

@login_required
def profile(request):
    user_posts = Item.objects.filter(created_by_id = request.user.id).order_by('-created_at')
    return render(request, 'register/profile.html', {'user_posts': user_posts, 'show_profile_icon': False})


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'register/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'register/login.html'


def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UpdateProfile()

    args['form'] = form
    args['show_profile_icon'] = False
    return render(request, 'register/update_profile.html', args)
