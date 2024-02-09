from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category,
    Comments,
    Genre,
    Title,
    Review)
from reviews.constants import FIELD_LEN_150, FIELD_LEN_254
from users.functions import UserValidateMixin, sending_confirmation_code
from users.models import User


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializers(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    genre = GenreSerializers(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True, default='0')

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class TitleSerializers(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_null=True,
        allow_empty=True)

    class Meta:
        fields = (
            'name', 'year', 'description', 'genre', 'category'
        )
        model = Title

    def to_representation(self, title):
        return TitleReadSerializers(title).data


class CommentsSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class ReviewsSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class UserSerializer(serializers.ModelSerializer):

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
        except IntegrityError as e:
            raise serializers.ValidationError({'detail': str(e)})
        sending_confirmation_code(user)
        return user

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

    def validate(self, data):
        username = data.get('username')
        if not username:
            raise serializers.ValidationError('Требуется имя пользователя.')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Код подтверждения невалиден')
        token = {'token': str(AccessToken.for_user(user))}
        return token
