from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["is_admin"] = user.is_superuser
        return token


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]
