# Generated by Django 4.1.6 on 2023-03-06 08:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0007_alter_item_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=models.ImageField(default=None, upload_to=""),
        ),
    ]
