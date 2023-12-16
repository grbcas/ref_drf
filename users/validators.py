import re
from rest_framework.validators import ValidationError

from users.models import User


class OnlyPhoneNumber(ValidationError):
    """Validate phone number"""
    def __call__(self, value) -> None:
        phone = re.sub(r'\b\D', '', value)
        clear_phone = re.sub(r'[\ \(\+]?', '', phone)

        if not bool(re.findall(r'^[7|8]*?\d{10}$', clear_phone) and len(clear_phone) == 11):
            raise ValidationError(f'Incorrect phone number: {value}')


class CheckIfKeyExists(ValidationError):
    """Check if invite_key exists"""
    def __call__(self, value) -> None:
        is_invite_key = User.objects.filter(own_invite_key=value).exists()
        if is_invite_key is False:
            raise ValidationError(f'There is no such key: {value}')
