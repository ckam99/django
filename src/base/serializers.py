from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Confirmation
import datetime


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'fullname',
                  'password', 'token', 'last_login')
        read_only_fields = ('token', 'password', 'email', 'username')

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class ConfirmEmailSerializer(serializers.Serializer):
    """Serializers confirmation email requests."""
    email = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('id', 'email',  'confirmed_at', 'token')

    def validate(self, data):
        email = data.get('email', None)
        token = data.get('token', None)

        if token is None:
            raise serializers.ValidationError(
                'A token is required to log in.'
            )
        confirmer = Confirmation.objects.filter(
            email=email, code=token).first()

        if confirmer:
            diff_date = datetime.datetime.now() - confirmer.created_at.replace(tzinfo=None)
            if diff_date.total_seconds() > 86400:
                raise serializers.ValidationError(
                    'Your confirmation token is expirated.'
                )
        else:
            raise serializers.ValidationError(
                'corrupted credentials'
            )
        if email:
            user = User.objects.filter(email=email).first()
            if user is None:
                raise serializers.ValidationError(
                    'An email address is required to log in.'
                )
            user.confirmed_at = datetime.datetime.now()
            user.save()
            confirmer.delete()
        else:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        return data
