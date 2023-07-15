from django import forms

from .models import Review, Ticket


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class CreateReviewForm(forms.ModelForm):
    """Form to create a review without a ticket"""

    rating = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={"class": "form-control radio-select-control", "min": 0, "max": 5},
        ),
        choices=[(str(x), x) for x in range(6)],
    )

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {
            "headline": "Titre",
            "rating": "Note",
            "body": "Commentaire",
        }
        widgets = {
            "headline": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }
