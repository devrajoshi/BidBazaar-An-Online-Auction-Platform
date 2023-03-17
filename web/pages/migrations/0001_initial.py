# Generated by Django 4.1.7 on 2023-03-16 11:40

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
            name="User",
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
                ("is_email_verified", models.BooleanField(default=False)),
                (
                    "email_token",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("avatar", models.CharField(blank=True, max_length=255, null=True)),
                ("last_modified", models.DateTimeField(blank=True, null=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("pan_no", models.PositiveIntegerField(blank=True, null=True)),
                ("citizen_no", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("image", models.ImageField(blank=True, upload_to="")),
                ("price", models.BigIntegerField()),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("deadline_at", models.DateTimeField(blank=True)),
                ("slug", models.CharField(max_length=255)),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bid",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=8)),
                ("bid_at", models.DateTimeField(auto_now_add=True)),
                (
                    "bidder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pages.item"
                    ),
                ),
            ],
        ),
    ]
