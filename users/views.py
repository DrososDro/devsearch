from django.shortcuts import render
from .models import Profile


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
