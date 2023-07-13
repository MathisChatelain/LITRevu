from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateTicketForm, CreateReviewForm
from django.db.models import Value, CharField
from .models import Ticket, Review
from .utils import get_users_viewable_reviews, get_users_viewable_tickets


@login_required
def home(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(request, "review/home.html", context={"posts": posts})


@login_required
def posts(request):
    return render(request, "review/posts.html")


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
                user=request.user,
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
    create_ticket_form = CreateTicketForm()
    create_review_form = CreateReviewForm()
    message = ""
    if request.method == "POST":
        create_ticket_form = CreateTicketForm(request.POST)
        create_review_form = CreateReviewForm(request.POST)
        if create_review_form.is_valid() and create_ticket_form.is_valid():
            # We create the ticket
            ticket: Ticket = Ticket.objects.create(
                title=create_ticket_form.cleaned_data["title"],
                description=create_ticket_form.cleaned_data["description"],
                image=create_ticket_form.cleaned_data["image"],
            )
            ticket.save()
            # We create the review
            review: Review = Review.objects.create(
                headline=create_review_form.cleaned_data["headline"],
                rating=create_review_form.cleaned_data["rating"],
                body=create_review_form.cleaned_data["body"],
                user=request.user,
                ticket=ticket,
            )
            review.save()
            return redirect("home")
    return render(
        request,
        "review/create-review.html",
        context={
            "create_review_form": create_review_form,
            "create_ticket_form": create_ticket_form,
            "message": message,
        },
    )
