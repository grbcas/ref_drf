from django.core.management import BaseCommand

from users.models import User
import os


class Command(BaseCommand):
    """create admin user from credentials from the .env file"""

    def handle(self, *args, **options):

        user, created = User.objects.get_or_create(
            username=os.getenv('ADMIN_USERNAME', 'admin'),
            phone_number='0',
            is_staff=True,
            is_superuser=True
        )
        if created:
            user.set_password(os.getenv('ADMIN_PASSWORD', 'admin@admin.admin'))
            user.save()
            return f'{user.username} was created'
