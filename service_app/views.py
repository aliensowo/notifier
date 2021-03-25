from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from . import models
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

                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('main/account/confirm_mail.txt', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()

                messages.success(request, "Registration successful. Please confirm your email address to complete the registration")
                return redirect("service_app:personal_page")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = forms.NewUserForm
        return render(request=request, template_name=self.template_name, context={"register_form": form})


class ConfirmEmail(TemplateView):

    def dispatch(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            typeUser = models.TypeUser.objects.get(user_id=user.id)
            typeUser.confirmation_email = True
            typeUser.save()
            # login(request, user)
            # return redirect('home')
            messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
            return redirect('service_app:personal_page')
        else:
            messages.error(request, 'Activation link is invalid!')
            return redirect('service_app:personal_page')


class PersonalView(TemplateView):
    template_name = 'main/personal_page.html'
    login_url = '/'

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if self.request.user:
            person = User.objects.get(username=self.request.user)
            if person.is_superuser or person.is_staff:
                return redirect('admin:index')
        user = User.objects.get(username=str(self.request.user))
        typeUser = models.TypeUser.objects.get(user_id=user.id)
        context['user'] = user
        context['type_user'] = typeUser

        return render(request, self.template_name, context)


class PrivacyView(TemplateView):
    template_name = 'main/privacy_page.html'

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PasswordReset(TemplateView):

    template_name = 'main/account/password_reset.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "main/account/password_reset_email.txt"
                        c = {
                            "email": user.email,
                            'domain': '127.0.0.1:8000',
                            'site_name': 'Website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect("/password_reset/done/")
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name=self.template_name,
                      context={"password_reset_form": password_reset_form})
