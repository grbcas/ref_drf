from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client
import os


class CreateAdminCommandTestCase(TestCase):

    def test_createadmin(self):

        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD', 'admin@admin.admin')
        call_command('createadmin')
        c = Client()
        is_logged_in = c.login(username=username, password=password)
        self.assertEqual(is_logged_in, True)
