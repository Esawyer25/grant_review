# Generated by Django 2.0.1 on 2018-01-20 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CapApp', '0041_auto_20180118_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='related_grant',
            name='core_project_num',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
