from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitleSerializers,
    TitleReadSerializers,
    CommentsSerializers,
    ReviewsSerializers)
from users.permissions import IsAthorModeraterAdmin
from reviews.models import Categories, Genres, Title, Comments, Reviews

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
