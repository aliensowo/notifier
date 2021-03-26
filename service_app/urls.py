"""notifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from .decorators import check_recaptcha
from . import views

app_name = 'service_app'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login_page'),
    path('signin', check_recaptcha(views.SigninView.as_view()), name='signin_page'),
    path('logout', views.LogoutView.as_view(), name='logout_apge'),
    path('personal', login_required(views.PersonalView.as_view(), login_url='/'), name='personal_page'),
    path('privacy', views.PrivacyView.as_view(), name='privacy_page'),
    path("password_reset", views.PasswordReset.as_view(), name="password_reset"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.ConfirmEmail.as_view(), name='activate'),
]
