# Generated by Django 5.0.7 on 2024-08-10 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_industry_service_industry_service_job_type'),
        ('artisans', '0014_artisan_industry_artisan_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='artisan',
            name='pay',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='artisan',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='industry_type', to='api.industry'),
        ),
    ]
