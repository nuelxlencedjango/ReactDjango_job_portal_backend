# Generated by Django 5.0.7 on 2024-08-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_industry_service_industry_service_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='pay_budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
