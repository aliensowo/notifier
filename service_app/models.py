from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class TypeUser(models.Model):
    """
    Дополнительная модель для расширения аттрибутов пользоваля
    """
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


class ApiRequestsHistory(models.Model):
    """
    Модель для хранения истории обращений к API
    """
    addr = models.CharField(name='addr', verbose_name='Адрес обращения', max_length=16)
    api_key = models.CharField(name='api_key', verbose_name='Ключ API', max_length=256)
    date_request = models.DateTimeField(name='date_request', verbose_name='Дата обращения', default=datetime.now())
    response = models.TextField(name='response', verbose_name='Тело ответа', null=True, blank=True)
    owner_api_key_id = models.ForeignKey(TypeUser, on_delete=models.CASCADE, verbose_name='Владелец ключа API', null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'История обращения к API'
        verbose_name_plural = 'История обращения к API'

    def __str__(self):
        if self.status:
            return str('[OK] ' + self.addr + ' to api [' + self.api_key + ']')
        else:
            return str('[FAILED] ' + self.addr + ' to api [' + self.api_key + ']')
