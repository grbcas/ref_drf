from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from rest_framework.generics import CreateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsOwner, IsProfileOwner
from users.serializers import UserSerializer
from users.tasks import task_send_code
from users.services import generate_string


class UserCreateAPIView(CreateAPIView):
    """New user creation"""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """set атрибут password для сохранения в виде хеша """

        # user = super().perform_create(serializer)
        user = serializer.save()

        if user is not None:
            password = self.request.data['password']
            user.set_password(password)
            code = generate_string(4)
            user.verification_code = code
            # command for adding task in celery query
            task_send_code.s(code=code).apply_async(countdown=1)

            user.save()
        return user


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        """set invite_key and related_user"""
        # user = self.request.user
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        if user.invite_key:
            raise ValidationError('invite_key is not empty')

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user.related_user = User.objects.exclude(own_invite_key=None).\
                get(own_invite_key=user.invite_key)
            user.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(TokenObtainPairView):
    """Authentication via token"""
    def post(self, request: Request, *args, **kwargs) -> Response:
        """add private key at the first login"""
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            # generate own_invite_key
            phone_number = request.data.get('phone_number')
            user = User.objects.get(phone_number=phone_number)
            user.add_own_invite_key()
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserVerification(GenericAPIView):
    """activate user with valid verification_code"""
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = request.data.get('phone_number')
        user = User.objects.get(phone_number=phone_number)
        if user.verification_code == request.data.get('verification_code'):
            user.is_active = True
            print(user.__dict__)
            user.save()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# class UserProfile(viewsets.ModelViewSet):

class UserProfile(ListAPIView):
    permission_classes = [IsProfileOwner]
    serializer_class = UserSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = User.objects.values('phone_number').filter(related_user=pk)
        print(queryset)
        return queryset

    # def get_object(self):
    #     print(self.queryset.values('phone_number'))
    #     return self.queryset.values('phone_number')
