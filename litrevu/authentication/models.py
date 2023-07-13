from django.db import models
from django.contrib.auth.models import User as AbstractUser


class User(AbstractUser):
    user_follows = models.ManyToManyField(
        to="self", symmetrical=False, related_name="followed_by", blank=True
    )
