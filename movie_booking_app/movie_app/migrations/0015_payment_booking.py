# Generated by Django 5.1.1 on 2024-12-25 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_app", "0014_banner_upcomingmovies"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="booking",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="movie_app.bookings",
            ),
        ),
    ]