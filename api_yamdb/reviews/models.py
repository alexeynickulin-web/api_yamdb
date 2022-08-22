from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .utils import username_not_me


class User(AbstractUser):
    CHOICES = [(1, 'user'), (2, 'admin'), (3, 'moderator')]
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator(), username_not_me],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },)
    confirmation_code = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=CHOICES, default='user')
    bio = models.CharField(max_length=200, default='')
