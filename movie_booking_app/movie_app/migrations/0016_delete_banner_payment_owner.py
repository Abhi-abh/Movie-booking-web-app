# Generated by Django 5.1.1 on 2024-12-26 03:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_app", "0015_payment_booking"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Banner",
        ),
        migrations.AddField(
            model_name="payment",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="movie_app.customer",
            ),
        ),
    ]
