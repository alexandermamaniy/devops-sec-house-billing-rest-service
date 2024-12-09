
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import ast
from users.models import User
from faker import Faker
fake = Faker()

class JwtTestCase(APITestCase):

    def setUp(self):
        self.admin_email = fake.email()
        self.user_email = fake.email()
        self.user_password = fake.password()
        self.admin_password = fake.password()
        # set url JWT
        self.url = reverse("token_obtain_pair")
        # create superuser
        self.superuser = User.objects.create_superuser(email=self.admin_email, password=self.admin_password)
        self.superuser.save()
        # create user
        self.user = User.objects.create_user(email=self.user_email, password=self.user_password)
        self.user.save()

    def test_create_user(self):
        user = User.objects.get(email=self.user_email)
        self.assertIsNotNone(user)
        self.assertEqual(self.user, user)
        self.assertNotEqual(user.password, self.user_password)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.get( email=self.admin_email)
        self.assertIsNotNone(superuser)
        self.assertEqual(self.superuser, superuser)
        self.assertNotEqual(superuser.password, self.admin_password)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


    def test_get_jwt(self):
        credentials = {
                'email': self.admin_email,
                'password': self.admin_password,
            }
        response = self.client.post( self.url, credentials, format="json")
        content = ast.literal_eval(response.content.decode("UTF-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(content['access'])
        self.assertIsNotNone(content['refresh'])