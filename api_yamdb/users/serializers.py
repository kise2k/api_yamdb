from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework import serializers

from reviews.constants import FIELD_LEN_150, FIELD_LEN_254
from .functions import UserValidateMixin, sending_confirmation_code
from .models import User


class UserSerializer(serializers.ModelSerializer,
                     UserValidateMixin):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio',
        )


class SignUpSerializer(serializers.Serializer, UserValidateMixin):

    username = serializers.CharField(
        max_length=FIELD_LEN_150,
        required=True
    )
    email = serializers.EmailField(
        max_length=FIELD_LEN_254,
        required=True
    )

    def create(self, validated_data):
        try:
            user, _ = User.objects.get_or_create(**validated_data)
            sending_confirmation_code(user)
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({'detail': str(e)})

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer, UserValidateMixin):

    username = serializers.CharField(
        max_length=FIELD_LEN_150,
        required=True,
    )

    confirmation_code = serializers.CharField(
        max_length=FIELD_LEN_150,
        required=True,
    )

    def validate_confirmation_code(self, value):
        username = self.initial_data.get('username')
        if not username:
            raise serializers.ValidationError('Требуется имя пользователя.')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, value):
            raise serializers.ValidationError('Код подтверждения невалиден')
        return value
