from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title, User


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'text',
        'score',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('author', 'title')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'review',
        'text',
        'pub_date'
    )
    search_fields = ('review',)
    list_filter = ('author', 'review')
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
UserAdmin.list_display = ('email', 'username', 'first_name',
                          'last_name', 'role', 'bio', 'is_superuser')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'
