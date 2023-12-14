from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView, LoginView, UserVerification, UserProfile
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/registration/', UserCreateAPIView.as_view(), name='user_registration'),
    path('api/verification/', UserVerification.as_view(), name='user_verification'),

    path('api/user/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user'),

    path('api/user/profile/<int:pk>/', UserProfile.as_view({'get': 'list'}), name='user_profile'),

]
