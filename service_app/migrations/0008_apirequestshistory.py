# Generated by Django 3.1.7 on 2021-03-26 10:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0007_auto_20210326_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiRequestsHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=16, verbose_name='Адрес обращения')),
                ('api_key', models.CharField(max_length=256, verbose_name='Ключ API')),
                ('date_request', models.DateTimeField(default=datetime.datetime(2021, 3, 26, 13, 4, 34, 280698), verbose_name='Дата обращения')),
                ('response', models.TextField(verbose_name='Тело ответа')),
                ('owner_api_key_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_app.typeuser', verbose_name='Владелец ключа API')),
            ],
            options={
                'verbose_name': 'История обращения к API',
                'verbose_name_plural': 'История обращения к API',
            },
        ),
    ]
