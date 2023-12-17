from django.core.management import BaseCommand

from users.models import User
import os


class Command(BaseCommand):
    """create admin user from credentials from the .env file"""

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            phone_number=os.getenv('PHONE_NUMBER'),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        print(user, created)
        if created:
            user.set_password(os.getenv('ADMIN_PASSWORD'))
            user.save()
            return f'admin {user.phone_number} was created'
