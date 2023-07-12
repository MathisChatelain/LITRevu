from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "review/home.html")


@login_required
def posts(request):
    return render(request, "review/posts.html")


@login_required
def following(request):
    return render(request, "review/following.html")
