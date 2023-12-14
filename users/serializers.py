from rest_framework import serializers
from django.contrib.auth import authenticate

from users.validators import OnlyPhoneNumber, CheckKeyActivation, CheckIfKeyExists
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(max_length=12, validators=[OnlyPhoneNumber()])
    invite_key = serializers.CharField(default=None, max_length=6, validators=[CheckIfKeyExists()])

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
