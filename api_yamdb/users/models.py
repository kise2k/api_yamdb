from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import ADMIN, MODERATOR, ROLES, USER


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True
    )
    email = models.EmailField(
        'Почта пользователя', max_length=254, unique=True
    )
    first_name = models.CharField(
        'Имя', max_length=150, null=True
    )
    last_name = models.CharField(
        'Фамилия', max_length=150, null=True
    )
    bio = models.TextField(
        'О себе', null=True
    )
    role = models.SlugField('роль пользователя', choices=ROLES, default=USER)
    confirmation_code = models.TextField('Код подтверждения', null=True)

    def check_user(self):
        return self.role == USER

    def check_admin(self):
        return self.role == ADMIN

    def check_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
