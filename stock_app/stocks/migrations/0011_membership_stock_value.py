# Generated by Django 2.0.3 on 2020-07-31 17:06

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0010_remove_transaction_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='stock_value',
            field=models.DecimalField(decimal_places=2, default=Decimal('10000.00'), max_digits=20),
        ),
    ]
