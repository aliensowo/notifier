# Generated by Django 3.1.7 on 2021-03-25 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0002_typeuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeuser',
            name='api key',
            field=models.CharField(blank=True, max_length=256, verbose_name='API Key'),
        ),
    ]
