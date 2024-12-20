# Generated by Django 5.1.1 on 2024-11-24 06:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookings",
            name="movie",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="movie_app.movie",
            ),
        ),
    ]
