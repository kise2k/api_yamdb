import csv
from typing import Any

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import (
    Category,
    Comments,
    Genre,
    Title_Genre,
    Title,
    Review
)
from users.models import User

CSV_FILES = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': Title_Genre,
    'review.csv': Review,
    'comments.csv': Comments,
}


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов в БД'

    def handle(self, *args: Any, **options: Any) -> str | None:
        for file, model in CSV_FILES.items():
            try:
                with open(
                    f'./static/data/{file}',
                    encoding='utf-8'
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    model.objects.bulk_create(model(**dict) for dict in reader)
                self.stderr.write(f'Данные из файла {file} успешно загружены')

            except FileNotFoundError:
                self.stderr.write(f'Файл {file} не найден')
            except IntegrityError:
                self.stderr.write(f'Файл {file} уже был загружен')
