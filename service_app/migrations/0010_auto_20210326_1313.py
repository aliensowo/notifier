# Generated by Django 3.1.7 on 2021-03-26 10:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0009_auto_20210326_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apirequestshistory',
            name='date_request',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 26, 13, 13, 5, 615965), verbose_name='Дата обращения'),
        ),
        migrations.AlterField(
            model_name='apirequestshistory',
            name='owner_api_key_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service_app.typeuser', verbose_name='Владелец ключа API'),
        ),
        migrations.AlterField(
            model_name='apirequestshistory',
            name='response',
            field=models.TextField(blank=True, null=True, verbose_name='Тело ответа'),
        ),
    ]