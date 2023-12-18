from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.validators import OnlyPhoneNumber, CheckIfKeyExists
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(
        max_length=12,
        validators=[OnlyPhoneNumber()]
    )

    invite_key = serializers.HiddenField(
        default=None,
        validators=[CheckIfKeyExists()],
    )

    verification_code = serializers.HiddenField(
        default=None,
        validators=[CheckIfKeyExists()],
    )

    class Meta:
        model = User
        fields = (
            'pk',
            'password',
            'phone_number',
            'invite_key',
            'verification_code'
        )

    def create(self, validated_data):
        print(validated_data)
        user, created = User.objects.get_or_create(
            phone_number=validated_data['phone_number'],
        )
        # user = User(**validated_data)
        if created:
            user.set_password(validated_data['password'])
            user.save()
            return user

        raise ValidationError(
            f'User with {validated_data["phone_number"]} already exists'
        )
