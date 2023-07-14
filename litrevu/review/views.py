from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateTicketForm, CreateReviewForm
from django.db.models import Value, CharField
from .models import Ticket, Review
from .utils import get_users_viewable_for_model, get_current_user
from datetime import datetime
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
    return render(request, "review/following.html")


@login_required
def create_review(request):
    return render(request, "review/create-review.html")


@login_required
def create_ticket(request):
    create_ticket_form = CreateTicketForm()
    message = ""
    if request.method == "POST":
        create_ticket_form = CreateTicketForm(request.POST)
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
        context={"form": create_ticket_form, "message": message},
    )


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
            create_ticket_form = CreateTicketForm(request.POST)
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
