from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

from app.forms import SignUpForm


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