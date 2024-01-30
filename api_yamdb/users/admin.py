from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
    empty_value_display = '-empty-'
