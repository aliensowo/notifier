from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from . import forms


class LogoutView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        logout(request)


class LoginView(TemplateView):
    template_name = "main/login_page.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        form_login = forms.LoginForm()
        context['form'] = form_login

        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("service_app:personal_page")
            else:
                context['error'] = "Логин или пароль неправильные"

        return render(request, self.template_name, context)


class SigninView(TemplateView):
    template_name = "main/signin_page.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        form_signin = forms.SigninForm()
        context['form'] = form_signin

        if form_signin.is_valid():
            username = form_signin.cleaned_data['username']
            email = form_signin.cleaned_data['email']
            password = form_signin.cleaned_data['password']
            password2 = form_signin.cleaned_data['password2']

            if password == password2:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                return redirect(reverse('service_app:login_page'))

        return render(request, self.template_name, context)


class PersonalView(TemplateView):
    template_name = 'main/personal_page.html'

    def dispatch(self, request, *args, **kwargs):
        context = {}
        context['auth'] = True
        return render(request, self.template_name, context)


class PrivacyView(TemplateView):

    template_name = 'main/privacy_page.html'

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.template_name)