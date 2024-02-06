import re
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError


def sending_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ващ код подтверждения {confirmation_code}',
        from_email=f'{settings.DEFAULT_FROM_EMAIL}',
        recipient_list=(user.email,),
        fail_silently=False,
    )


class UserValidateMixin:
    regex = re.compile(r'^[\w.@+-]+\Z')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError(
                'Недопустимое имя пользователя'
            )
        if not self.regex.findall(value):
            raise ValidationError(
                ('Недопустимое имя пользователя')
            )
        return value
