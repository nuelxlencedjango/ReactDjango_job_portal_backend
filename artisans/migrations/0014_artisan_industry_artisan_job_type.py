# Generated by Django 5.0.7 on 2024-08-10 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artisans', '0013_alter_artisan_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='artisan',
            name='industry',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='artisan',
            name='job_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
