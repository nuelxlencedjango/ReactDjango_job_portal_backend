# Generated by Django 5.0.7 on 2025-02-12 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0010_remove_paymentinformation_customer_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentinformation',
            name='transaction_id',
            field=models.CharField(default='0', max_length=100, unique=True),
        ),
    ]
