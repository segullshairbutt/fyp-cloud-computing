from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt

from users.serializers import CustomTokenObtainPairSerializer, SignupSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return HttpResponse(status=status.HTTP_201_CREATED)


class ListUsers(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if 'username' in self.request.GET:
            return User.objects.filter(username=self.request.GET['username'])
        else:
            return User.objects.all()


@api_view(['PUT'])
def change_password(request):
    password = request.data["password"]
    user = request.user

    user.set_password(password)
    user.save()

    return HttpResponse(status=status.HTTP_200_OK)


def email_now(email, form_id):
    message = f"""Click on the link below to reset your password. 
{settings.FRONT_END_APP}/?id={form_id}"""

    send_mail("Reset Password for Smart Scaling App", message, settings.EMAIL_HOST_USER, [email], fail_silently=False)


@api_view(['POST'])
def forget_password(request):
    email = request.data['email']
    username = request.data['username']
    users = User.objects.filter(username=username)

    if not users:
        response = Response(data={"error": "user with this username not found."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = users[0]

        if user.email and user.email != email:
            response = Response(data={"error": "this email don't exist in our records"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            token = jwt.encode({"id": user.id}, settings.SECRET_KEY, "HS256")
            email_now(email, token)
            user.email = email

            user.save()

            response = Response(status=status.HTTP_200_OK)

    return response


@api_view(['POST'])
def change_password_by_token(request):
    token = request.data['token']
    password = request.data['password']

    decoded_token = jwt.decode(token, settings.SECRET_KEY, "HS256")
    user_id = decoded_token['id']

    user = User.objects.get(id=user_id)
    user.set_password(password)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
