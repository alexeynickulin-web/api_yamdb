from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Год произведения не может быть больше текущего.'
        )


def username_not_me(value):
    if value.lower() == 'me':
        raise ValidationError("You cannot use 'me' as a username")
    return value
