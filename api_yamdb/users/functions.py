import re

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError

from reviews.constants import REGEX_ALLOWS, REGEX_PATTERN


def sending_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ващ код подтверждения {confirmation_code}',
        from_email=f'{settings.DEFAULT_FROM_EMAIL}',
        recipient_list=(user.email,),
        fail_silently=False,
    )


def validate_username(value):
    regex = re.compile(REGEX_PATTERN)
    if value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя me запрещено'
        )
    if not regex.findall(value):
        raise ValidationError(
            (f'Разрешены символы: {REGEX_ALLOWS}')
        )
    return value


class UserValidateMixin:
    @staticmethod
    def validate_username(value):
        return validate_username(value)
