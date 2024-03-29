# Generated by Django 2.0.3 on 2020-07-21 19:31

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.BooleanField(default=False)),
                ('date_join', models.DateField(default=django.utils.timezone.now)),
                ('total_asset_value', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=20)),
                ('rank', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(50)])),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='ROOM_<built-in function id>', editable=False, max_length=50)),
                ('create_date', models.DateField(default=django.utils.timezone.now)),
                ('members', models.ManyToManyField(through='stocks.Membership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Saved_Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('initial_price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.BooleanField(default=False)),
                ('quantity', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=20)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('ticker', models.CharField(default='', max_length=20, null=True)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.Room')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Room'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
