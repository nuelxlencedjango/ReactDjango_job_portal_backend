# Generated by Django 5.0.7 on 2024-12-28 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0002_jobdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobdetails',
            name='added_at',
        ),
        migrations.RemoveField(
            model_name='jobdetails',
            name='artisan',
        ),
    ]
