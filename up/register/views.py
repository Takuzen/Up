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
from ..users.models import User, FriendShip


# Create your views here.
def register(response):
    model = get_user_model()
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                response, f'{username}さんのアカウントが登録されました！ 右上からプロフィールも追加しよう！')
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
    img_obj_lis = []
    for post in user_posts:
        post_img = Images.objects.filter(item_id=post.id).last()
        try:
            is_video = post_img.image.url.endswith(('.MOV', '.mp4'))
        except:
            is_video = False
        img_obj_lis.append({'img': post_img, 'is_video': is_video})
    posts_cnt = len(user_posts)

    followees_cnt = len(User.objects.filter(
        id=request.user.id).first().followees.all())
    followers_cnt = len(User.objects.filter(
        id=request.user.id).first().followers.all())

    render_dict = {'user_posts': user_posts,
                   'show_profile_icon': False,
                   'posts_cnt': posts_cnt,
                   'followees_cnt': followees_cnt,
                   'followers_cnt': followers_cnt,
                   'img_obj_lis': img_obj_lis}
    return render(request, 'register/profile.html', render_dict)


def user_portfolio(request, id):
    portfolio_owner = User.objects.get(id=id)
    user_posts = Item.objects.filter(
        created_by_id=id).order_by('-created_at')
    img_obj_lis = []
    for post in user_posts:
        post_img = Images.objects.filter(item_id=post.id).last()
        try:
            is_video = post_img.image.url.endswith(('.MOV', '.mp4'))
        except:
            is_video = False
        img_obj_lis.append({'img': post_img, 'is_video': is_video})

    posts_cnt = len(user_posts)
    followees_cnt = len(User.objects.get(
        id=id).followees.all())
    followers_cnt = len(User.objects.get(
        id=id).followers.all())

    followee_id = User.objects.get(id=id).id
    print("me", request.user.id)
    print("other", id)
    try:
        follower_id = User.objects.get(id=request.user.id).id
    except:
        follower_id = followee_id
    print("follwoerids", follower_id, followee_id)
    if follower_id != followee_id:
        show_follow_button = True
    else:
        show_follow_button = False

    # if is_follow is above 0, it shows that there is a connection between the two
    is_following = len(FriendShip.objects.filter(
        followee_id=followee_id, follower_id=follower_id)) > 0
    print("isfollowing:", is_following)

    render_dict = {'user_posts': user_posts,
                   'show_profile_icon': False,
                   'posts_cnt': posts_cnt,
                   'followees_cnt': followees_cnt,
                   'followers_cnt': followers_cnt,
                   'img_obj_lis': img_obj_lis,
                   'portfolio_owner': portfolio_owner, 
                   'is_following': is_following,
                   'show_follow_button': show_follow_button}
    return render(request, 'register/user_portfolio.html', render_dict)


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
