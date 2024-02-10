from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    viewsets,
    mixins,
    permissions
)


from .serializers import (
    CategorySerializers,
    GenreSerializers,
    TitleSerializers,
    TitleReadSerializers,
    CommentsSerializers,
    ReviewsSerializers,
)
from .permission import (
    IsAthorModeraterAdmin,
    ReadOnly,
    IsAdmin,
)
from .filter import TitleFilter
from reviews.models import Category, Genre, Title, Review


class CategoryGenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (ReadOnly | IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class GenresViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name', 'year')
    permission_classes = (ReadOnly | IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializers
        return TitleSerializers


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializers
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAthorModeraterAdmin
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_title()
                        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAthorModeraterAdmin
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
