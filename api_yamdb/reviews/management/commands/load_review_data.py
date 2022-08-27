import csv

from django.core.management.base import BaseCommand
from reviews.models import Review


class Command(BaseCommand):
    """Класс для инициализации БД из csv файла."""

    def handle(self, *args, **options):
        """Запись в базу данных."""
        with open('static/data/review.csv', 'r', encoding='utf-8') as file:
            reviews = list(csv.DictReader(file, delimiter=','))
        # id, title_id, text, author, score, pub_date
        for review in reviews:
            print(review)
            review_to_save = Review(
                id=review['id'],
                title_id=review['title_id'],
                author_id=review.get('author'),
                text=review.get('text'),
                score=review.get('score'),
                pub_date=review.get('pub_date'),
            )
            review_to_save.save()
