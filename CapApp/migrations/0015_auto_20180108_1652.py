# Generated by Django 2.0.1 on 2018-01-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CapApp', '0014_auto_20180107_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grant_Publications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pmid', models.CharField(max_length=10, null=True)),
                ('project_number', models.CharField(max_length=12, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='grant',
            options={'ordering': ['-total_cost']},
        ),
        migrations.AlterField(
            model_name='grant',
            name='funding_ics',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
