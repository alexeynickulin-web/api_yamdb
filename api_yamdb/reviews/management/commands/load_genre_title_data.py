import csv

from django.core.management.base import BaseCommand
from reviews.models import TitleGenre


class Command(BaseCommand):
    """Класс для инициализации БД из csv файла."""

    def handle(self, *args, **options):
        """Запись в базу данных."""
        with open(
                'static/data/genre_title.csv', 'r', encoding='utf-8'
        ) as file:
            title_genres = list(csv.DictReader(file, delimiter=','))

        for title_genre in title_genres:
            print(title_genre)
            title_genre_to_save = TitleGenre(
                id=title_genre['id'],
                genre_id=title_genre['genre_id'],
                title_id=title_genre['title_id'],
            )
            title_genre_to_save.save()
