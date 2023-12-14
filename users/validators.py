import re
from rest_framework.validators import ValidationError

from users.models import User


class OnlyPhoneNumber(ValidationError):
    """Validate phone number"""
    def __call__(self, value) -> None:
        phone = re.sub(r'\b\D', '', value)
        clear_phone = re.sub(r'[\ \(\+]?', '', phone)

        if not bool(re.findall(r'^[7|8]*?\d{10}$', clear_phone) and len(clear_phone) == 11):
            raise ValidationError(f'Incorrect phone number ')


class CheckKeyActivation(ValidationError):
    """Check key activation"""
    def __call__(self, value) -> None:
        # invite_key = user.invite_key
        print(value, self.__dict__)
        # if invite_key:
        #     raise ValidationError(f'The invite_key is already set')


class CheckIfKeyExists(ValidationError):
    """CHeck if invite_key exists"""
    def __call__(self, value) -> None:
        is_invite_key = User.objects.filter(own_invite_key=value).exists()
        print('invite_keys', is_invite_key)
        if is_invite_key is False:
            print(ValidationError(f'There is no such key'))
            raise ValidationError(f'There is no such key')
#
# if __name__ == '__main__':
#     OnlyPhoneNumber('').__call__('+071112223344')
