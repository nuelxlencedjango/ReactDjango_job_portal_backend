# Generated by Django 5.0.7 on 2024-07-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artisans', '0002_remove_artisan_years_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artisan',
            name='profession',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
