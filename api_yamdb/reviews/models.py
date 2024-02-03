from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_year

User = get_user_model()


class Categories(models.Model):
    """Модель описывающая категории."""
    name = models.CharField(
        max_length=256,
        verbose_name='Имя категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Уникальный идентификатор категории'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:25]


class Genres(models.Model):
    """Модель описывает Жанры."""
    name = models.CharField(
        max_length=256,
        verbose_name='Имя жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Уникальный идентификатор жанра'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:25]


class Title(models.Model):
    """Модель описывающая произведения, к которым пишут отзывы"""
    name = models.CharField(
        max_length=256,
        verbose_name='Имя произведения'
    )
    year = models.IntegerField(
        validators=(validate_year,),
        verbose_name='Год создания',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genres = models.ManyToManyField(
        Genres,
        verbose_name='Жанр'
    )
    categories = models.ForeignKey(
        Categories,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ('year',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Reviews(models.Model):
    """Модель описывающая отзывы."""
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Оценка(1-10)',
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение',
        
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )

    class Meta:
        ordering = ('pub_date',)
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:25]


class Comments(models.Model):
    """Модель описывающая комментарии."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        verbose_name='отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comment'
        ordering = ('pub_date', )

    def __str__(self):
        return self.name[:25]
