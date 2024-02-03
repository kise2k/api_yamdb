from rest_framework import filters, viewsets, permissions, mixins
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import MethodNotAllowed

from .serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitleSerializers,
    TitleReadSerializers,
    CommentsSerializers,
    ReviewsSerializers)
from users.permissions import IsAthorModeraterAdmin, ReadOnly, IsAdmin, AnonimReadOnly
from reviews.models import Categories, Genres, Title, Comments, Reviews


class CategoriesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Categories.objects.all()
    permission_classes = (ReadOnly | IsAdmin, )
    serializer_class = CategoriesSerializers
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializers
    permission_classes = (ReadOnly | IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (AnonimReadOnly | IsAdmin,)

    def get_serializer_class(self):
        if self.action == ('create', 'update', 'partial_update',):
            return TitleSerializers
        return TitleReadSerializers

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializers
    permission_classes = (IsAthorModeraterAdmin,)
    pagination_class = PageNumberPagination
    
    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))
    
    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
    
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializers
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAthorModeraterAdmin
    )
    pagination_class = PageNumberPagination
    
    def get_review(self):
        return get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
    
    def get_queryset(self):
        return self.get_review().comment.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")
