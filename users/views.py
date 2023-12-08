from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """New user creation"""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# переопределяем атрибут password для сохранения в виде хеша
    def perform_create(self, serializer):
        user = super().perform_create(serializer)

        if user is not None:
            password = self.request.data['password']
            user.set_password(password)
            user.save()
        return user
