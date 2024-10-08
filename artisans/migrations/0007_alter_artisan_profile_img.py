# Generated by Django 5.0.7 on 2024-07-26 07:22

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artisans', '0006_alter_artisan_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artisan',
            name='profile_img',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
    ]
