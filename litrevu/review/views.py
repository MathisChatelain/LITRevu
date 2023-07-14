from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateTicketForm, CreateReviewForm
from django.db.models import Value, CharField
from .models import Ticket, Review
from .utils import get_users_viewable_for_model, get_current_user
from datetime import datetime
from authentication.forms import FollowUserForm
from authentication.models import User


@login_required
def home(request):
    reviews = get_users_viewable_for_model(request.user, Review)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = get_users_viewable_for_model(request.user, Ticket)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(request, "review/home.html", context={"posts": posts})


@login_required
def posts(request):
    user = get_current_user(request.user)
    reviews = Review.objects.filter(user=user)
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = Ticket.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(request, "review/posts.html", context={"posts": posts})


@login_required
def following(request):
    user = get_current_user(request.user)
    users_followed = user.user_follows.exclude(username=user.username).all()
    followers = User.objects.filter(user_follows__in=[user]).exclude(
        username=user.username
    )
    follow_user_form = FollowUserForm()
    message = ""
    if request.method == "POST":
        follow_user_form = FollowUserForm(request.POST)

        if follow_user_form.is_valid():
            user_to_follow = User.objects.filter(
                username=follow_user_form.cleaned_data["username"]
            )
            if len(user_to_follow) > 0:
                message = "Cet utilisateur n'existe pas."
                user.user_follows.add(user_to_follow[0])
                user.save()
                message = f"Vous suivez maintenant {user_to_follow[0].username}."
            # reset users_followed
            users_followed = user.user_follows.exclude(username=user.username).all()
    return render(
        request,
        "review/following.html",
        context={
            "follow_user_form": follow_user_form,
            "message": message,
            "users_followed": users_followed,
            "followers": followers,
        },
    )


@login_required
def create_review(request):
    return render(request, "review/create-review.html")


@login_required
def create_ticket(request):
    """Allows a user to create or update a ticket"""
    create_ticket_form = CreateTicketForm()
    if request.GET.get("ticket_id"):
        existing_ticket = Ticket.objects.get(id=request.GET.get("ticket_id"))
        create_ticket_form = CreateTicketForm(instance=existing_ticket)
    message = ""
    if request.method == "POST":
        create_ticket_form = (
            CreateTicketForm(request.POST, request.FILES)
            if not create_ticket_form
            else create_ticket_form
        )
        if create_ticket_form.is_valid():
            # We create the ticket
            ticket: Ticket = Ticket.objects.create(
                title=create_ticket_form.cleaned_data["title"],
                description=create_ticket_form.cleaned_data["description"],
                image=create_ticket_form.cleaned_data["image"],
                user=get_current_user(request.user),
                time_created=datetime.now(),
            )
            ticket.save()
            return redirect("home")
    return render(
        request,
        "review/create-ticket.html",
        context={
            "form": create_ticket_form,
            "message": message,
            "ticket": existing_ticket if request.GET.get("ticket_id") else None,
        },
    )


@login_required
def unfollow_user(request):
    user = get_current_user(request.user)
    user_to_unfollow = User.objects.filter(id=request.GET.get("user_id"))
    if request.method == "GET":
        user.user_follows.remove(user_to_unfollow[0])
        user.save()
    return redirect("following")


@login_required
def remove_ticket(request):
    user = get_current_user(request.user)
    ticket_to_remove = Ticket.objects.filter(id=request.GET.get("ticket_id"))
    if request.method == "GET":
        if ticket_to_remove[0].user == user:
            ticket_to_remove.delete()
    return redirect("posts")


@login_required
def create_review(request):
    """Allows a user to create a review with or without a ticket"""
    create_review_form = CreateReviewForm()
    ticket_id = request.GET.get("ticket_id", None)
    ticket: Ticket = Ticket.objects.get(id=ticket_id) if ticket_id else None
    create_ticket_form = (
        CreateTicketForm(instance=ticket) if ticket else CreateTicketForm()
    )
    message = ""
    if request.method == "POST":
        if not ticket:
            create_ticket_form = CreateTicketForm(request.POST, request.FILES)
        create_review_form = CreateReviewForm(request.POST)
        user = get_current_user(request.user)
        if create_review_form.is_valid() and (create_ticket_form.is_valid() or ticket):
            # We create the ticket in case it does not exist
            if not ticket:
                ticket: Ticket = Ticket.objects.create(
                    title=create_ticket_form.cleaned_data["title"],
                    description=create_ticket_form.cleaned_data["description"],
                    image=create_ticket_form.cleaned_data["image"],
                    user=user,
                    time_created=datetime.now(),
                )
            ticket.has_response = True
            ticket.save()
            # We create the review
            review: Review = Review.objects.create(
                headline=create_review_form.cleaned_data["headline"],
                rating=create_review_form.cleaned_data["rating"],
                body=create_review_form.cleaned_data["body"],
                user=user,
                ticket=ticket,
                time_created=datetime.now(),
            )
            review.save()
            return redirect("home")
    return render(
        request,
        "review/create-review.html",
        context={
            "create_review_form": create_review_form,
            "create_ticket_form": create_ticket_form,
            "ticket": ticket,
            "message": message,
        },
    )
