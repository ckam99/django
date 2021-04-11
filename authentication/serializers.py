from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        max_length=60, min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=60, required=False)
    last_name = serializers.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name', 'password')

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already un use')})
        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
