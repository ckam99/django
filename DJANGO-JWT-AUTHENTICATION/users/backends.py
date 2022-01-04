import jwt
from django.conf import settings
from rest_framework import authentication as auth, exceptions
from django.contrib.auth.models import User


class JWTAuthentication(auth.BaseAuthentication):

    def authenticate(self, request):
        credentials = auth.get_authorization_header(request)
        if not credentials:
            return None
        token_type, token = credentials.decode('utf-8').split(' ')
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms='HS256')
            user = User.objects.get(username=payload['username'])
            return (user, token)
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed("Your token is invalid")
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed("Your token is expire")

        return super().authenticate(request)
