from django.contrib import admin

from .models import Categories, Genres, Title, Reviews, Comments


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    list_display = ('name', 'slug')
    search_fields = ('name',)
    empty_value_display = 'пусто'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    list_display = ('name', 'slug')
    search_fields = ('name',)
    empty_value_display = 'пусто'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_filter = ('name', 'categories')
    list_display = ('name', 'year', 'description', 'categories')
    search_fields = ('name', 'description')
    empty_value_display = 'пусто'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_filter = ('pub_date', 'author')
    list_display = ('text', 'score', 'pub_date', 'title', 'author')
    search_fields = ('author', 'pub_date')
    empty_value_display = 'пусто'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_filter = ('author', )
    list_display = ('text', 'author', 'review', 'pub_date')
    search_fields = ( 'pub_date', 'author')
    empty_value_display = 'пусто'
