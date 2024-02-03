import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Обработка получения года создания."""
    if (value > dt.datetime.now()) or (value < 0):
        return ValidationError(
            'Введен неккоректный год создания. \
            Он не должен превышать текущий и не может быть меньше 0'
        )
