# Generated by Django 4.1.4 on 2023-03-01 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(default=None, upload_to='uploads/'),
        ),
    ]
