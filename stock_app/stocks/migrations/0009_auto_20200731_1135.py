# Generated by Django 2.0.3 on 2020-07-31 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0008_auto_20200731_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
