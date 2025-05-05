from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('profit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('volume', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('winrate', models.IntegerField(default=0)),
                ('rank_total_profit', models.IntegerField(default=0)),
                ('rank_total_volume', models.IntegerField(default=0)),
                ('rank_monthly_profit', models.IntegerField(default=0)),
                ('rank_monthly_volume', models.IntegerField(default=0)),
                ('rank_weekly_profit', models.IntegerField(default=0)),
                ('rank_weekly_volume', models.IntegerField(default=0)),
                ('medals', models.JSONField(default=list)),
                ('avatar', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')], default=1)),
                ('job', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('favorite_subject', models.CharField(blank=True, default='Not specified', max_length=100)),
            ],
        ),
    ]
