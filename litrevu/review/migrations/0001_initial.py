# Generated by Django 4.0.4 on 2023-07-15 09:40

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(default="", max_length=128)),
                ("description", models.CharField(default="", max_length=500)),
                ("image", models.ImageField(blank=True, upload_to="images")),
                ("has_response", models.BooleanField(default=False)),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to="authentication.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("headline", models.CharField(max_length=128)),
                ("body", models.CharField(blank=True, max_length=8192)),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="review.ticket"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentication.user",
                    ),
                ),
            ],
        ),
    ]
