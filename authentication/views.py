from django.conf import settings
from django.contrib import auth
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,
from .serializers import UserSerializer, LoginSerializer
import jwt


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user:
            token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY)
            serializer = UserSerializer(user)
            data = {'meta': serializer.data, 'access_token': token}
            return Response(data)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CurrentUserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(str(request.user))
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
