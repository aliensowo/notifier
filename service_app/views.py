from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from . import forms


class LogoutView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('service_app:login_page')


class LoginView(TemplateView):
    template_name = "main/login_page.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("service_app:personal_page")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name=self.template_name, context={"login_form": form})


class SigninView(TemplateView):
    template_name = "main/signin_page.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            form = forms.NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("service_app:personal_page")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = forms.NewUserForm
        return render(request=request, template_name=self.template_name, context={"register_form": form})


class PersonalView(TemplateView):
    template_name = 'main/personal_page.html'

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PrivacyView(TemplateView):

    template_name = 'main/privacy_page.html'

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.template_name)