# Generated by Django 2.0.3 on 2020-07-31 17:10

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0011_membership_stock_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='stock_value',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=20),
        ),
    ]
