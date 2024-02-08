from datetime import datetime

from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)

from .constants import (
    LENGTH_FOR_ADMIN,
    NAME_CONST_CHAR,
    SLUG_CONST_CHAR,
    MIN_CONST_SCORE_VALUE,
    MAX_CONST_SCORE_VALUE,
    MIN_COSNT_FOR_YEAR,
)
from users.models import User


class CategoryAndGenre(models.Model):
    """Абстрактная модель, описывающая категории и жанры."""
    name = models.CharField(
        max_length=NAME_CONST_CHAR,
        verbose_name='Название',
        db_index=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=SLUG_CONST_CHAR,
        verbose_name='Уникальный идентификатор',
    )

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        return self.name[:LENGTH_FOR_ADMIN]


class Category(CategoryAndGenre):
    """Модель описывающая категории."""

    class Meta(CategoryAndGenre.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryAndGenre):
    """Модель описывающая жанры."""

    class Meta(CategoryAndGenre.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель описывающая произведения, к которым пишут отзывы"""
    name = models.CharField(
        max_length=NAME_CONST_CHAR,
        verbose_name='Имя произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_COSNT_FOR_YEAR,
                message='Значение года не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
        verbose_name='Год создания',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('year',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:LENGTH_FOR_ADMIN]


class ReviewAndCommentsBase(models.Model):
    """Абстрактный базовый класс для моделей Review и Comment."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        abstract = True
        ordering = ('pub_date', )

    def __str__(self):
        return self.text[:LENGTH_FOR_ADMIN]


class Review(ReviewAndCommentsBase):
    """Модель описывающая отзывы."""
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                MAX_CONST_SCORE_VALUE,
                message='Введенная оценка выше допустимой'
            ),
            MinValueValidator(
                MIN_CONST_SCORE_VALUE,
                message='Введенная оценка ниже допустимой'
            )
        ],
        verbose_name='Оценка(1-10)',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta(ReviewAndCommentsBase.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title',),
                name='unique_author_title'
            ),
        )
        default_related_name = 'reviews'


class Comments(ReviewAndCommentsBase):
    """Модель описывающая комментарии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(ReviewAndCommentsBase.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comment'
