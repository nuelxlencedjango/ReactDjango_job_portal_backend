# Generated by Django 5.0.7 on 2025-02-26 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='website',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
