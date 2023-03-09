# Generated by Django 4.1.6 on 2023-03-06 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pages", "0002_alter_user_citizen_no_alter_user_pan_no"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="seller",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]