from .serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitleSerializers,
    TitleReadSerializers)
from rest_framework import filters, viewsets
from reviews.models import Categories, Genres, Title
from rest_framework.pagination import PageNumberPagination


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
