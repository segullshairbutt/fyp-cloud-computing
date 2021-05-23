from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from users.views import (
    CustomTokenObtainPairView, SignupView, ListUsers, forget_password, change_password, change_password_by_token)


urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', SignupView.as_view()),
    path('forgot', forget_password),
    path('change-password', change_password),
    path('change-password/token', change_password_by_token),
    path('users', ListUsers.as_view(), name='list_users'),
]
