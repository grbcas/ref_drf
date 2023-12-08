import re
from rest_framework.validators import ValidationError


class OnlyPhoneNumber(ValidationError):

    def __call__(self, value) -> bool:
        phone = re.sub(r'\b\D', '', value)
        clear_phone = re.sub(r'[\ \(\+]?', '', phone)

        if not bool(re.findall(r'^[7|8]*?\d{10}$', clear_phone) and len(clear_phone) == 11):
            raise ValidationError(f'Incorrect phone number ')

#
# if __name__ == '__main__':
#     OnlyPhoneNumber('').__call__('+071112223344')
