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
import uuid
from . import models
from . import forms


class LogoutView(TemplateView):
    """
    Class based view для логаута пользователя
    """

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('service_app:login_page')


class LoginView(TemplateView):
    """
    Class based view для логина пользователя
    """

    template_name = "main/login_page.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Функция обработки запросов со страницы логина
        Получаем post запрос с формы на странице и производим логин пользователя
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
    """
    Class based view для регистрации пользователя
    """

    template_name = "main/signin_page.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Функция обработки запросов со страницы регистрации

        Принимая форму:
            1. Валидация капчи
            2. Валидация данных пользователя + валидация екстар атрибутов пользователя
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.method == "POST":
            form = forms.NewUserForm(request.POST)
            if self.request.recaptcha_is_valid:
                if form.is_valid() and form.cleaned_data:
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
    """
    Class based view для подтверждения e-mail пользователя
    """

    def dispatch(self, request, uidb64, token, *args, **kwargs):
        """
        Функция обработки запроса по адресу подтверждения почты пользователя

        Происходит обработка get парметров, которые генерируются при отправке сообщения и состовляют ссылку подтверждения
        При успешной попыткой меняем статус подтверждения почты в моделе пользователя
        :param request:
        :param uidb64:
        :param token:
        :param args:
        :param kwargs:
        :return:
        """
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
    """
    Class based view страницы пользователя (доступна только авторизированным пользователям)
    """

    template_name = 'main/personal_page.html'
    login_url = '/'

    def dispatch(self, request, *args, **kwargs):
        """
        Функция обработки страницы
        логика:
            1. отобразить api ключ
            2. сгенерировать ключ
            3. обновить существующий ключ
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        context = {}
        if self.request.user:
            person = User.objects.get(username=self.request.user)
            if person.is_superuser or person.is_staff:
                return redirect('admin:index')
        user = User.objects.get(username=str(self.request.user))
        typeUser = models.TypeUser.objects.get(user_id=user.id)
        context['user'] = user
        context['type_user'] = typeUser
        if typeUser.api_key is not None:
            context['value_key'] = typeUser.api_key
        if request.method == 'POST':
            api_key = uuid.uuid4()
            context['value_key'] = api_key
            typeUser.api_key = api_key
            typeUser.save()
            return redirect('service_app:personal_page')

        return render(request, self.template_name, context)


class PrivacyView(TemplateView):
    """
    Class based view страницы политики кофиденциальности
    """
    template_name = 'main/privacy_page.html'

    def dispatch(self, request, *args, **kwargs):
        """
        рендр страницы
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return render(request, self.template_name)


class PasswordReset(TemplateView):
    """
    Class based view сброса пароля
    """

    template_name = 'main/account/password_reset.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Функция сброса пароля
        ЛогикаЖ
            1. принимаем и валидируем форму\
            2. находим пользователя по email из формы
            3. генерируем письмо со сслыкой для сброса пароля
            4. отправляем письмо
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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


class ApiMethod(TemplateView):
    """
    Class based view предложенного апи метода
    """

    def dispatch(self, request, token, *args, **kwargs):
        """
        Логика:
            получаем IP с которого обращаются
            получаем токен по которому обращаюстя

            ищем токен в БД
                1. отображаем данные пользователя при успешном нахождении такого с 200 кодом ответа
                    1.1 записываем в историю обращении всю информацию по запросу
                2. отображем "None" с 404 кодом ответа
                    2.1 записываем в историю обращений информацию о неудачном обращении
        :param request:
        :param token:
        :param args:
        :param kwargs:
        :return:
        """
        context = {}
        data = {}

        data['addr'] = self.get_client_ip()
        data['api_key'] = token

        try:
            typeUser = models.TypeUser.objects.get(api_key=token)
            user = User.objects.get(id=typeUser.user_id)
            context['email'] = user.email
            context['username'] = user.username

            data['response'] = context
            data['owner_api_key_id'] = typeUser
            data['status'] = True

            history_add = models.ApiRequestsHistory(**data)
            history_add.save()

            return HttpResponse('{}'.format(context), status=200)
        except models.TypeUser.DoesNotExist:

            history_add = models.ApiRequestsHistory(**data)
            history_add.save()

            return HttpResponse('None', status=404)

    def get_client_ip(self):
        """
        Метод получения IP пользоввтеля
        :return:
        """
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
