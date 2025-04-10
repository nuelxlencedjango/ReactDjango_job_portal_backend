from django.db import migrations
from decimal import Decimal

def calculate_commissions(apps, schema_editor):
    ArtisanProfile = apps.get_model('acct', 'ArtisanProfile')
    for artisan in ArtisanProfile.objects.exclude(pay__isnull=True):
        # Only calculate if commission isn't already set
        if artisan.commission is None:
            commission = round(artisan.pay * Decimal('0.10'), 2)
            artisan.commission = commission
            artisan.pay += commission
            artisan.save(update_fields=['commission', 'pay'])

class Migration(migrations.Migration):
    dependencies = [
        ('acct', '0016_artisanprofile_commission'),
    ]

    operations = [
        migrations.RunPython(calculate_commissions),
    ]