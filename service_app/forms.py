from django import forms
from django.conf import settings
from django.core.mail import send_mail
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from . import models


class NewUserForm(UserCreationForm):
    """
    Форма создания нового пользователя
    """
    email = forms.EmailField(required=True)
    phone = PhoneNumberField(widget=forms.TextInput(attrs={
        'value': '+7'
    }))

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def check_data(self):
        """
        дополнительная валидация номера телефона
        :return:
        """
        try:
            typeUser = models.TypeUser.objects.get(phone=self.cleaned_data['phone'])
            msg = 'user with this phone number ({}) already exist'.format(typeUser.phone)
            return False
        except models.TypeUser.DoesNotExist:
            return True

    def save(self, commit=True):
        """
        Метод сохранения/добавления пользователя
        :param commit:
        :return:
        """
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            newUser = User.objects.get(email=self.cleaned_data['email'])
            more = models.TypeUser(
                user_id=newUser.id,
                phone=self.cleaned_data['phone']
            )
            more.save()
        return user




