# Generated by Django 5.0.7 on 2024-12-11 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acct', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artisanprofile',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='employerprofile',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='managerprofile',
            name='date_joined',
        ),
    ]
