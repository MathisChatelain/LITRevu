"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from authentication.views import login_page, logout_user, signup
from review.views import (
    create_review,
    create_ticket,
    following,
    home,
    posts,
    remove_review,
    remove_ticket,
    unfollow_user,
    update_review,
    update_ticket,
)

urlpatterns = [
    # auth
    path("admin/", admin.site.urls),
    path("", login_page, name="login"),
    path("logout/", logout_user, name="logout"),
    path("signup/", signup, name="signup"),
    # review
    path("home/", home, name="home"),
    path("posts/", posts, name="posts"),
    path("following/", following, name="following"),
    path("create-review/", create_review, name="create-review"),
    path("create-ticket/", create_ticket, name="create-ticket"),
    path("unfollow-user/", unfollow_user, name="unfollow-user"),
    path("remove-ticket/", remove_ticket, name="remove-ticket"),
    path("update-ticket/", update_ticket, name="update-ticket"),
    path("remove-review/", remove_review, name="remove-review"),
    path("update-review/", update_review, name="update-review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
