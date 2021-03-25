from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField()

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        more = models.TypeUser.objects.create(
            confirmation_email=False,
            api_key='',
            user_id=user.id,
            phone=self.cleaned_data['phone']
        )
        if commit:
            user.save()
        return user

    def send_mail(self):

        SUBJECT = 'NOTIFIER: Уведомление!'
        TEXT_MESASGE = 'Уважаемый {}, Вам пришло личное сообщение от заказчика. '.format(self.email)
        send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [self.email])
