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

from ..app.models import Item, Images
from .models import Profile
from ..users.models import User


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
    user_posts = Item.objects.filter(
        created_by_id=request.user.id).order_by('-created_at')
    print(user_posts)
    img_objects = []
    for post in user_posts:
        print(post.id)
        img_objects.append(Images.objects.filter(item_id=post.id).first())
    posts_cnt = len(user_posts)
    print(posts_cnt)
    followees_cnt = len(User.objects.filter(
        id=request.user.id).first().followees.all())
    followers_cnt = len(User.objects.filter(
        id=request.user.id).first().followers.all())
    print(img_objects)
    render_dict = {'user_posts': user_posts,
                   'show_profile_icon': False,
                   'posts_cnt': posts_cnt,
                   'followees_cnt': followees_cnt,
                   'followers_cnt': followers_cnt,
                   'img_obj': img_objects}
    return render(request, 'register/profile.html', render_dict)


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
        user = User.objects.get(id=request.user.id)
        try:
            profile_image = request.FILES['image']
        except:
            profile_image = user.image
        request.FILES.update({'image': profile_image})
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            user = form.save(commit=False)
            user.image = request.FILES['image']
            user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UpdateProfile(instance=request.user)

        args['image'] = request.user.image

    args['form'] = form
    args['show_profile_icon'] = False
    return render(request, 'register/update_profile.html', args)
