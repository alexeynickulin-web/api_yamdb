import csv

from django.core.management.base import BaseCommand
from reviews.models import User


class Command(BaseCommand):
    """Класс для инициализации БД из csv файла."""

    def handle(self, *args, **options):
        """Запись в базу данных."""
        with open('static/data/users.csv', 'r', encoding='utf-8') as file:
            users = list(csv.DictReader(file, delimiter=','))

        for user in users:
            user = User(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                role=user.get('role'),
                bio=user.get('bio'),
                first_name=user.get('first_name'),
                last_name=user.get('last_name'),
            )
            user.save()
