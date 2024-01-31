from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать зто Имя пользователя'
            )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать зто Имя пользователя'
            )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmatetion_code = serializers.CharField(
        max_length=100, required=True
    )

    class Meta:
        model = User
        fielda = ('username', 'confirmatetion_code')
