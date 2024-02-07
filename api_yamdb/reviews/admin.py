from django.contrib import admin

from .models import Category, Genre, Title, Review, Comments


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    """Настройка админ панели для категории."""
    list_filter = ('name', )
    list_display = ('name', 'slug')
    search_fields = ('name',)
    empty_value_display = 'пусто'


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    """Настройка админ панели для жанров."""
    list_filter = ('name', )
    list_display = ('name', 'slug')
    search_fields = ('name',)
    empty_value_display = 'пусто'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка админ панели для произведений."""
    list_filter = ('name', 'category')
    list_display = ('name', 'year', 'description', 'category', 'get_genres')
    search_fields = ('name', 'description')
    empty_value_display = 'пусто'

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка админ панели для отзывов."""
    list_filter = ('pub_date', 'author')
    list_display = ('text', 'score', 'pub_date', 'title', 'author')
    search_fields = ('author', 'pub_date')
    empty_value_display = 'пусто'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Настройка админ панели для комментариев."""
    list_filter = ('author', )
    list_display = ('text', 'author', 'review', 'pub_date')
    search_fields = ('pub_date', 'author')
    empty_value_display = 'пусто'
