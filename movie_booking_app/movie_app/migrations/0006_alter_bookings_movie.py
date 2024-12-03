# Generated by Django 5.1.1 on 2024-11-24 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_app", "0005_alter_bookings_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookings",
            name="movie",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="movie_app.movie",
            ),
        ),
    ]
