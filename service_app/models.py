from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class TypeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(name='phone', verbose_name='Телефон', unique=True)
    confirmation_email = models.BooleanField(
        name='confirmation_email',
        verbose_name='Подтвежденный пользователь',
        default=False
    )
    api_key = models.CharField(
        name='api_key',
        verbose_name='API Key',
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.user.email)
