from django.db import models
from django.contrib.auth.models import User


class TypeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(name='phone', verbose_name='Телефон')
    confirmation_email = models.BooleanField(
        name='confirmation email',
        verbose_name='Подтыежденный пользователь',
        default=False
    )
    api_key = models.CharField(
        name='api key',
        verbose_name='API Key',
        max_length=256,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.user.email)
