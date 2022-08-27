import csv

from django.core.management.base import BaseCommand
from reviews.models import Title


class Command(BaseCommand):
    """Класс для инициализации БД из csv файла."""

    def handle(self, *args, **options):
        """Запись в базу данных."""
        with open('static/data/titles.csv', 'r', encoding='utf-8') as file:
            titles = list(csv.DictReader(file, delimiter=','))

        for title in titles:
            print(title)
            title = Title(
                id=title['id'],
                name=title['name'],
                year=title.get('year'),
                category_id=title.get('category'),
            )
            title.save()
