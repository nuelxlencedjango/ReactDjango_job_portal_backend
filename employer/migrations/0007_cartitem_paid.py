# Generated by Django 5.0.7 on 2025-02-04 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0006_alter_cartitem_employer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
