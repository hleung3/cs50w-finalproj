# Generated by Django 2.0.3 on 2020-07-31 15:26

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_auto_20200727_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='cash_remaining',
            field=models.DecimalField(decimal_places=2, default=Decimal('10000.00'), max_digits=20),
        ),
    ]
