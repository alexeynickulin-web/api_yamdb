from django.core.exceptions import ValidationError


def username_not_me(value):
    if value == 'me':
        raise ValidationError("You cannot use 'me' as a username")
    return value
