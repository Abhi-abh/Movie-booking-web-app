# Generated by Django 5.1.1 on 2024-12-07 13:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_app", "0011_rename_image_bookings_qr_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookings",
            name="qr_code",
            field=models.ImageField(null=True, upload_to="qr_codes/"),
        ),
    ]
