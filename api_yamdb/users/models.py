from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.constants import (
    FIELD_LEN_150,
    FIELD_LEN_254,
    USER, ADMIN, MODERATOR, ROLES
)
from .functions import validate_username


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=FIELD_LEN_150,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        verbose_name='Почта пользователя',
        max_length=FIELD_LEN_254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=FIELD_LEN_150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=FIELD_LEN_150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    role = models.CharField(
        verbose_name='роль пользователя',
        max_length=max([len(value) for value, _ in ROLES]),
        choices=ROLES,
        default=USER
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
