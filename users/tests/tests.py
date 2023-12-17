from django.core.management import call_command
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test.client import Client
import os

from rest_framework import status


class CreateAdminCommandTestCase(TestCase):

    def test_createadmin(self):
        #   os.getenv('PHONE_NUMBER', '8') ->  ('8',)
        phone_number = '8'
        password = os.getenv('ADMIN_PASSWORD', 'admin@admin.admin')
        print(phone_number, password)
        call_command('createadmin')
        c = Client()
        is_logged_in = c.login(phone_number=phone_number, password=password)
        self.assertEqual(is_logged_in, True)


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('users:user_registration')

    def test_user_registration_phone(self):

        data_wrong_phone = {
            'phone_number': '99993332211',
            'password': 'user_pswd',
        }

        response = self.client.post(self.url, data=data_wrong_phone)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"phone_number": [
                             "Incorrect phone number: 99993332211"
                         ]})

    def test_user_registration_none_user(self):
        """if user is not None:"""
        response = self.client.post(self.url, data=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration(self):

        valid_data = {
            'phone_number': '89993332211',
            'password': 'user_pswd',
        }

        response = self.client.post(self.url, data=valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.json().get('phone_number'),
              valid_data.get('phone_number'))
        self.assertEqual(response.json().get('phone_number'),
                         {valid_data.get('phone_number')})
