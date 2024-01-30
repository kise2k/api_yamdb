from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import ADMIN, MODERATOR, ROLES, USER


class User(AbstractUser):
    username = models.CharField(
        'имя пользователя', max_length=50, unique=True
    )
    email = models.EmailField(
        'почта пользователя', max_length=100, unique=True
    )
    role = models.SlugField('роль пользователя', choices=ROLES, default=USER)
    confirmation_code = models.TextField('код подтверждения', null=True)

    class Meta:
        ordering = ('username')

    def check_admin(self):
        return (
            self.role == ADMIN or self.is_staff or self.is_superuser
        )

    def check_moderator(self):
        return (
            self.role == MODERATOR or self.is_staff or self.is_superuser
        )
