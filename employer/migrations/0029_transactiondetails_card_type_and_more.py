# Generated by Django 5.0.7 on 2025-03-16 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0028_remove_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiondetails',
            name='card_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='device_fingerprint',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='first_6digits',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='flutter_app_fee',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='flutter_card_issuer',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='flutter_settled_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='flutter_transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='flutter_transaction_ref_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='ip_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transactiondetails',
            name='last_4digits',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
