from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitleSerializers,
    TitleReadSerializers,
    CommentsSerializers,
    ReviewsSerializers
    )
from reviews.models import Categories, Genres, Title, Comments, Reviews
from users.permissions import IsAthorModeraterAdmin


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializers
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == ('create', 'update', 'partial_update'):
            return TitleSerializers
        return TitleReadSerializers


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializers
    permission_classes = (IsAthorModeraterAdmin,)
    pagination_class = PageNumberPagination
    
    def get_review(self):
        return get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
    
    def get_queryset(self):
        return self.get_review.comment.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
    


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializers
    permission_classes = (IsAthorModeraterAdmin,)
    pagination_class = PageNumberPagination
    
    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))
    
    def get_queryset(self):
        return self.get_title().titles.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())