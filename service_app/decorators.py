from django.conf import settings
from django.contrib import messages

import requests


def check_recaptcha(function):
    """
    Функция-декоратор для проверки рекапчи
        1. Из запроса получаем информацию об ответе о валидации каптчи
        2. Отправляем запрос на сервер Google для верификации сайта и получения окончательного результата валидации
    :param function:
    :return:
    """
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap