from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=16, widget=forms.TextInput(attrs={
        'class': 'login__input',
        'name': 'username',
        'placeholder': 'Имя пользователя',
    }))
    password = forms.CharField(max_length=100,
                               label='',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'login__input',
                                   'name': 'password',
                                   'placeholder': 'Пароль',
                               }))


class SigninForm(forms.Form):
    username = forms.CharField(label='', max_length=16, widget=forms.TextInput(attrs={
        'class': 'signin__input',
        'name': 'username',
        'placeholder': 'Имя пользователя',
    }))
    email = forms.EmailField(label='', max_length=120, widget=forms.EmailInput(attrs={
        'class': 'signin__input',
        'name': 'email',
        'placeholder': 'e-mail',
    }))
    password = forms.CharField(max_length=100,
                               label='',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'signin__input',
                                   'name': 'password',
                                   'placeholder': 'Пароль',
                               }))
    password2 = forms.CharField(max_length=100,
                                label='',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'signin__input',
                                    'name': 'password2',
                                    'placeholder': 'Повтор пароля',
                                }))