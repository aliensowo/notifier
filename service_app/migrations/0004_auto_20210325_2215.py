# Generated by Django 3.1.7 on 2021-03-25 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0003_auto_20210325_2209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='typeuser',
            old_name='api key',
            new_name='api_key',
        ),
        migrations.RemoveField(
            model_name='typeuser',
            name='confirmation email',
        ),
        migrations.AddField(
            model_name='typeuser',
            name='confirmation_email',
            field=models.BooleanField(default=False, verbose_name='Подтвежденный пользователь'),
        ),
    ]