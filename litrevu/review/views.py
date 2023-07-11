from django.shortcuts import render


def hello(request):
    return render(request, "review/home.html", {"name": "timéo"})
