# Generated by Django 2.0.1 on 2018-01-15 21:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CapApp', '0030_auto_20180115_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='related_grants',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=500, null=True), default=[], null=True, size=None),
        ),
    ]
