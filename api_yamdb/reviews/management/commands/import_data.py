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

csv_files = {
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
        for file, model in csv_files.items():
            try:
                for row in csv.DictReader(open(f'./static/data/{file}')):
                    if file == 'users.csv':
                        model.objects.create(
                            id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                        )
                    elif file == 'genre.csv' or file == 'category.csv':
                        model.objects.create(
                            id=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                    elif file == 'titles.csv':
                        model.objects.create(
                            id=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category=Category.objects.get(id=row['category']),
                        )
                    elif file == 'genre_title.csv':
                        model.objects.create(
                            id=row['id'],
                            title_id=row['title_id'],
                            genre_id=row['genre_id'],
                        )
                    elif file == 'review.csv':
                        model.objects.create(
                            id=row['id'],
                            title_id=row['title_id'],
                            text=row['text'],
                            author=User.objects.get(id=row['author'],),
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                    elif file == 'comments.csv':
                        model.objects.create(
                            id=row['id'],
                            review_id=row['review_id'],
                            text=row['text'],
                            author=User.objects.get(id=row['author'],),
                            pub_date=row['pub_date'],
                        )
                self.stderr.write(f'Данные из файла {file} успешно загружены')

            except FileNotFoundError:
                self.stderr.write(f'Файл {file} не найден')
            except IntegrityError:
                self.stderr.write(f'Файл {file} уже был загружен')
