from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile


def login_user(request):
    if request.user.is_authenticated:
        return redirect("profiles")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, "users/login_register.html")


def logout_user(request):
    logout(request)
    messages.error(request, "User was succesfully logout")
    return redirect("login")


def profiles(request):
    profile = Profile.objects.all()
    context = {
        "users": profile,
    }
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    print(top_skills)
    other_skills = profile.skill_set.filter(description="")
    context = {
        "user": profile,
        "topSkills": top_skills,
        "otherSkills": other_skills,
    }
    return render(request, "users/user-profile.html", context)
