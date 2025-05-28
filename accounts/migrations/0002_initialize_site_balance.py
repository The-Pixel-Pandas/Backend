from django.db import migrations
from decimal import Decimal

def initialize_site_balance(apps, schema_editor):
    SiteBalance = apps.get_model('accounts', 'SiteBalance')
    SiteBalance.objects.create(balance=Decimal('1000000.00'))

def reverse_site_balance(apps, schema_editor):
    SiteBalance = apps.get_model('accounts', 'SiteBalance')
    SiteBalance.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initialize_site_balance, reverse_site_balance),
    ] 