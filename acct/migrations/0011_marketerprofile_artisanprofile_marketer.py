# Generated by Django 5.0.7 on 2025-03-10 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acct', '0010_remove_fingerprint_fingerprint_template'),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('date_joined', models.DateField(auto_now_add=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.area')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='artisanprofile',
            name='marketer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registered_artisans', to='acct.marketerprofile'),
        ),
    ]
