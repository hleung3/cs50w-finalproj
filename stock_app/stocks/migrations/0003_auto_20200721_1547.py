# Generated by Django 2.0.3 on 2020-07-21 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_auto_20200721_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]