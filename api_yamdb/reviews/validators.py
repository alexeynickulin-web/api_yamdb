from rest_framework.exceptions import ValidationError
from datetime import date


def validate_year(value):
    if value > date.today().year:
        raise ValidationError(
            'Год произведения не может быть больше текущего.'
        )
