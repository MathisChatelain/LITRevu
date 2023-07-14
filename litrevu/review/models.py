from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from authentication.models import User


class Ticket(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="tickets",
        null=True,
    )
    title = models.CharField(max_length=128, default="")
    description = models.CharField(max_length=500, default="")
    image = models.ImageField(upload_to="images", blank=True)
    has_response = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline}"

    def rating_as_stars(self):
        return "⭐" * self.rating
