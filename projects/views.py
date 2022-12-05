from django.shortcuts import render

# Create your views here.
projectslist = [
    {
        "id": "1",
        "title": "Ecomerce Website",
        "description": "Fully functional ecommerce website",
    },
    {
        "id": "2",
        "title": "Portofolio website",
        "description": "This was a project where i build out my Portofolio",
    },
    {
        "id": "3",
        "title": "Social Network",
        "description": "Awesome open source project I am still working",
    },
]


def projects(request):
    page = "projects"
    number = 5
    context = {
        "msg": page,
        "number": number,
        "projects": projectslist,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    projectobj = None
    for i in projectslist:
        if i["id"] == pk:
            projectobj = i

    return render(request, "projects/single-project.html", {"obj": projectobj})
