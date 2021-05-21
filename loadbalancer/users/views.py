from django.http import JsonResponse, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from django.contrib.auth.models import User

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
            user.is_developer = True
            user.save()
            return HttpResponse(status=status.HTTP_201_CREATED)


class ListUsers(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        try:
            is_developer = self.request.GET['is_developer']
        except MultiValueDictKeyError:
            is_developer = None

        if is_developer == 'true':
            query_set = User.objects.filter(is_developer=True)
        elif is_developer == 'false':
            query_set = User.objects.filter(is_developer=False)
        else:
            query_set = User.objects.all()

        return query_set
