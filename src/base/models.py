import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=60, null=True, blank=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        to_encode = {}
        expire = datetime.utcnow() + timedelta(minutes=60*1440)
        to_encode.update({
            'id': self.pk,
            "exp": expire
        })
        access_token = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm='HS256')
        return access_token
