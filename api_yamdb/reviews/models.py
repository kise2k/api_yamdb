from django.db import models


class Category(models.Model):
    name = models.TextField('Категория', max_length=256)
    slug = models.SlugField('Слаг катерогии', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Жанр', max_length=256)
    slug = models.SlugField('Слаг жанра', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField('Название произведения', max_length=256)
    year = models.IntegerField('Год создания')
    description = models.TextField('Описание')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория')
    genre = models.ManyToManyField(Genre,
                                   through='TitleGerne',
                                   verbose_name='Жанр')

    def __str__(self):
        return self.name


class TitleGerne(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
