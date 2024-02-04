from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    ADMIN,
    MODERATOR, ROLES, USER
)


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'Почта пользователя', max_length=254, unique=True
    )
    first_name = models.CharField(
        'Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True
    )
    bio = models.TextField(
        'О себе', blank=True
    )
    role = models.CharField(
        'роль пользователя', max_length=20, choices=ROLES, default=USER
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
