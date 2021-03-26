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

    def check_data(self):
        try:
            typeUser = models.TypeUser.objects.get(phone=self.cleaned_data['phone'])
            msg = 'user with this phone number ({}) already exist'.format(typeUser.phone)
            return False
        except models.TypeUser.DoesNotExist:
            return True

    def save(self, commit=True):
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




