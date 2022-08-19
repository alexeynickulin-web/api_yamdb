from django.db import models


class CustomUser(models.Model):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey()
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
