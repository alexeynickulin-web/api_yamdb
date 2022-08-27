import csv

from django.core.management.base import BaseCommand
from reviews.models import Genre


class Command(BaseCommand):
    """Класс для инициализации БД из csv файла."""

    def handle(self, *args, **options):
        """Запись в базу данных."""
        with open('static/data/genre.csv', 'r', encoding='utf-8') as file:
            genres = list(csv.DictReader(file, delimiter=','))

        for genre in genres:
            print(genre)
            genre_to_save = Genre(
                id=genre['id'],
                name=genre['name'],
                slug=genre.get('slug'),
            )
            genre_to_save.save()
