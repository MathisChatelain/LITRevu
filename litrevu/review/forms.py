from django import forms
from django.contrib.auth.models import User
from .models import Ticket, Review


class CreateTicketForm(forms.ModelForm):
    """Form to create a ticket"""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class CreateReviewForm(forms.ModelForm):
    """Form to create a review without a ticket"""

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {
            "headline": "Titre",
            "rating": "Note",
            "body": "Commentaire",
        }
