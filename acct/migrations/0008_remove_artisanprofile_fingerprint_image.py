# Generated by Django 5.0.7 on 2024-12-14 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acct', '0007_managerprofile_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artisanprofile',
            name='fingerprint_image',
        ),
    ]