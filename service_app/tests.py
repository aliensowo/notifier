from django.test import TestCase
import uuid
from django.contrib.auth.models import User
from service_app.models import TypeUser
from service_app.forms import NewUserForm


class ModelTest(TestCase):
    """
    Test creation a new user
    """
    username = 'qwerty'
    email = 'qwerty@mail.ru'
    password = 'Q123456789q'

    @classmethod
    def setUpTestData(cls):
        #
        User.objects.create(username=cls.username, email=cls.email, password=cls.password)
        user = User.objects.get(email=cls.email)
        TypeUser.objects.create(phone='4567893625', user_id=user.id)

    def test_creation(self):
        user = User.objects.get(id=1)
        typeUser = TypeUser.objects.get(user_id=1)
        self.assertEqual(user.id, typeUser.user_id)


class FormsTest(TestCase):
    """
    Test user creation and phone validation
    """
    username = 'qwerty'
    email = 'qwerty@mail.ru'
    password = 'Q123456789q'
    password2 = 'Q123456789q'
    password_not_eq = 'Q123456789r'
    password_short = '456789'
    phone1 = '79812224566'
    phone2 = '+12125552368'
    phone3 = '9813504317'

    def test_new_user(self):
        form_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password2,
            'phone': self.phone1
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data1 = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password2,
            'phone': self.phone2
        }
        form1 = NewUserForm(data=form_data1)
        self.assertTrue(form1.is_valid())


class ApiMethodTest(TestCase):
    """
    Test response code api_method's
    """
    username = 'qwerty'
    email = 'qwerty@mail.ru'
    password = 'Q123456789q'
    token = uuid.uuid4()

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username=cls.username, email=cls.email, password=cls.password)
        user = User.objects.get(email=cls.email)
        TypeUser.objects.create(phone='4567893625', user_id=user.id, api_key=cls.token)

    def test_response_200(self):
        resp = self.client.get('/api/{}'.format(self.token))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b"{'email': 'qwerty@mail.ru', 'username': 'qwerty'}")

    def test_response_404(self):
        resp = self.client.get('/api/{}'.format(uuid.uuid4()))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.content, b'None')


