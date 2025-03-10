# Generated by Django 5.1.1 on 2024-12-19 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movie_app", "0013_delete_orededitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
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
                ("image", models.ImageField(upload_to="images")),
            ],
        ),
        migrations.CreateModel(
            name="UpcomingMovies",
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
                ("title", models.CharField(max_length=200)),
                ("price", models.FloatField()),
                ("language", models.CharField(default=0, max_length=200)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="images")),
            ],
        ),
    ]
