import csv

from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    """Класс для инициализации БД из csv файла."""

    def handle(self, *args, **options):
        """Запись в базу данных."""
        with open('static/data/category.csv', 'r', encoding='utf-8') as file:
            catigories = list(csv.DictReader(file, delimiter=','))

        for category in catigories:
            print(category)
            category_to_save = Category(
                id=category['id'],
                name=category['name'],
                slug=category.get('slug'),
            )
            category_to_save.save()
