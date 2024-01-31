from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Categories, Comments, Genres, Title, Reviews


class CategoriesSerializers(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializers(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitleSerializers(serializers.ModelSerializer):
    categories = SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all())
    genres = SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializers(serializers.ModelSerializer):
    category = CategoriesSerializers(read_only=True)
    genres = GenresSerializers(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'discription', 'genre', 'category')
        model = Title


class CommentsSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class ReviewsSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews
