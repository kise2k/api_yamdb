from django.core.mail import send_mail

from .constants import TEST_EMAIL


def sending_confirmation_code(email, confirmation_code):
    send_mail(
        subject='Код подтверждения',
        message=f'Ващ код подтверждения {confirmation_code}',
        from_email=TEST_EMAIL,
        recipient_list=(email,),
    )
