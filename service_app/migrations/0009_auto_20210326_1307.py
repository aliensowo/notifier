# Generated by Django 3.1.7 on 2021-03-26 10:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0008_apirequestshistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='apirequestshistory',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='apirequestshistory',
            name='date_request',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 26, 13, 7, 36, 357802), verbose_name='Дата обращения'),
        ),
    ]
