from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from .constants import TEST_EMAIL


def sending_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ващ код подтверждения {confirmation_code}',
        from_email=f'{TEST_EMAIL}',
        recipient_list=(user.email,),
        fail_silently=False,
    )
