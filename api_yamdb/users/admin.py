from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .functions import UserValidateMixin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
        'bio',
    )
    list_editable = ('role',)
    search_fields = ('username',)
    empty_value_display = 'пусто'
