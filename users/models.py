from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


NULLABLE = {'null': True, 'blank': True}


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):

        if not phone_number:
            raise ValueError('Phone number is required')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """
    User model
    """

    username = models.CharField(max_length=6, unique=True, verbose_name='username', **NULLABLE)
    phone_number = models.CharField(max_length=12, unique=True, verbose_name='User phone number',)
    own_invite_key = models.CharField(max_length=6, unique=True, verbose_name='own_invite_key', **NULLABLE)
    alien_invite_key = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Related_key', **NULLABLE)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.pk} {self.phone_number}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
