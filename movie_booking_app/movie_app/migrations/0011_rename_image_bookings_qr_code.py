# Generated by Django 5.1.1 on 2024-12-07 09:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movie_app", "0010_bookings_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bookings",
            old_name="image",
            new_name="qr_code",
        ),
    ]