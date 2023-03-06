from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileModelForm


def login_user(request):
    page = "Login"
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
            messages.success(request, "succesfully Log In")
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect")
    context = {
        "page": page,
    }
    return render(request, "users/login_register.html", context)


def logout_user(request):
    logout(request)
    messages.info(request, "User was succesfully logout")
    return redirect("login")


def register_user(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "User account was created!")
            return redirect("edit-profile")
        else:
            messages.error(
                request,
                "An  error has occurred during registatation",
            )

    context = {
        "page": page,
        "form": form,
    }
    return render(request, "users/login_register.html", context)


def profiles(request):
    profile = Profile.objects.all()
    context = {
        "users": profile,
    }
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    context = {
        "user": profile,
        "topSkills": top_skills,
        "otherSkills": other_skills,
    }
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        "user": profile,
        "skills": skills,
        "projects": projects,
    }
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):

    curent_user = request.user.profile
    form = ProfileModelForm(instance=curent_user)
    if request.method == "POST":
        form = ProfileModelForm(request.POST, request.FILES, instance=curent_user)
        if form.is_valid():
            form.save()
            return redirect("account")
    context = {"user": form}
    return render(request, "users/profile_form.html", context)
