import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User
import base64
from django.contrib.auth import authenticate


class JWTBasicAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        header = authentication.get_authorization_header(request)
        if not header:
            return None
        header_type, credential = header.decode('utf-8').split(' ')
        if header_type in ['Token', 'Bearer']:
            return self.token_authenticate(credential)
        return self.basic_authenticate(credential)

    def token_authenticate(self, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Your token is invalid")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Your token is expire")

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'No user matching this token was found.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'This user has been deactivated.')
        return (user, token)

    def basic_authenticate(self, credential):
        if not credential:
            return None
        email, password = base64.b64decode(
            credential).decode("utf-8").split(':')

        user = authenticate(email=email.strip(), password=password.strip())
        if user is None:
            raise exceptions.AuthenticationFailed(
                'No user matching those credentials.')
        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'This user has been deactivated.')
        return (user, None)
