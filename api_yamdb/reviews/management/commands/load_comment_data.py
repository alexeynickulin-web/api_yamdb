import csv

from django.core.management.base import BaseCommand
from reviews.models import Comment


class Command(BaseCommand):
    """Класс для инициализации БД из csv файла."""

    def handle(self, *args, **options):
        """Запись в базу данных."""
        with open('static/data/comments.csv', 'r', encoding='utf-8') as file:
            comments = list(csv.DictReader(file, delimiter=','))

        for comment in comments:
            print(comment)
            comment_to_save = Comment(
                id=comment['id'],
                review_id=comment['review_id'],
                text=comment.get('text'),
                author_id=comment.get('author'),
                pub_date=comment.get('pub_date'),
            )
            comment_to_save.save()
