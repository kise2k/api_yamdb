import csv

from django.core.management.base import BaseCommand
from typing import Any

from reviews.models import Category, Comments, Genre, Title, Review
from users.models import User


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов в БД'

    def ImportUser(self):
        if User.objects.exists():
            print('Данные User уже загружены')
        else:
            for row in csv.DictReader(open('/users.csv')):
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],)
            print('Данные User загружены')

    def ImportTitle(self):
        if Title.objects.exists():
            print('Данные Title уже загружены')
        else:
            for row in csv.DictReader(open('/titles.csv')):
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),)
            print('Данные Title загружены')

    def ImportGenre(self):
        if Genre.objects.exists():
            print('Данные Genre уже загружены')
        else:
            for row in csv.DictReader(open('/genre.csv')):
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],)
            print('Данные Genre загружены')

    def ImportGenreTitle(self):
        if Genre.objects.exists():
            print('Данные GenreTitle уже загружены')
        else:
            for row in csv.DictReader(open('/genre_title.csv')):
                Genre.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],)
            print('Данные GenreTitle загружены')

    def ImportCategory(self):
        if Category.objects.exists():
            print('Данные Category уже загружены')
        else:
            for row in csv.DictReader(open('/category.csv')):
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],)
            print('Данные Categiory загружены')

    def ImportReview(self):
        if Review.objects.exists():
            print('Данные Review уже загружены')
        else:
            for row in csv.DictReader(open('/review.csv')):
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author'],),
                    score=row['score'],
                    pub_date=row['pub_date'],)
            print('Данные Review загружены')

    def ImportComments(self):
        if Comments.objects.exists():
            print('Данные Comments уже загружены')
        else:
            for row in csv.DictReader(open('/comments.csv')):
                Comments.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author'],),
                    pub_date=row['pub_date'],)
            print('Данные Comments загружены')

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.ImportCategory(),
        self.ImportGenre(),
        self.ImportGenreTitle(),
        self.ImportTitle(),
        self.ImportUser(),
        self.ImportReview(),
        self.ImportComments()
