from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreateTicketForm, CreateReviewForm
from .models import Ticket, Review


@login_required
def home(request):
    return render(request, "review/home.html")


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
    return render(
        request,
        "review/create-review.html",
        context={
            "create_review_form": create_review_form,
            "create_ticket_form": create_ticket_form,
            "message": message,
        },
    )
