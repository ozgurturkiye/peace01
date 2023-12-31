# Generated by Django 4.2.4 on 2023-08-24 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="English",
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
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "word_type",
                    models.CharField(
                        blank=True,
                        choices=[("A", "Adjective"), ("N", "Noun"), ("V", "Verb")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("synonyms", models.ManyToManyField(blank=True, to="words.english")),
            ],
        ),
        migrations.CreateModel(
            name="Turkish",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="WordBox",
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
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(
                        blank=True,
                        related_name="friends_wb",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("words", models.ManyToManyField(blank=True, to="words.english")),
            ],
        ),
        migrations.CreateModel(
            name="WordBoxDetail",
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
                ("answer_status", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "english",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="words.english"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wordbox",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="words.wordbox"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SingleWordGame",
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
                ("answer_status", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("number_of_play", models.PositiveIntegerField(default=0)),
                (
                    "english",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="words.english"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="english",
            name="translations",
            field=models.ManyToManyField(
                blank=True, related_name="translations", to="words.turkish"
            ),
        ),
        migrations.AddConstraint(
            model_name="wordboxdetail",
            constraint=models.UniqueConstraint(
                fields=("wordbox", "user", "english"),
                name="unique_wbd_wordbox_user_english",
            ),
        ),
        migrations.AddConstraint(
            model_name="wordbox",
            constraint=models.UniqueConstraint(
                fields=("name", "owner"), name="unique_wb_name_owner"
            ),
        ),
        migrations.AddConstraint(
            model_name="singlewordgame",
            constraint=models.UniqueConstraint(
                fields=("owner", "english"), name="unique_owner_english"
            ),
        ),
    ]
