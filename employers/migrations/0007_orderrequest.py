# Generated by Django 5.0.7 on 2024-08-20 02:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_service_pay_budget'),
        ('artisans', '0015_artisan_pay_alter_artisan_industry'),
        ('employers', '0006_remove_orderrequest_artisan_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('job_date', models.DateField()),
                ('preferred_time', models.TimeField()),
                ('contact_person', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('date_ordered', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('paid', models.BooleanField(default=False)),
                ('artisan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artisans.artisan')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employers.employer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.service')),
            ],
        ),
    ]
