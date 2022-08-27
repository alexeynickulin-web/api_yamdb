from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.utils import ROLES, USER


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise ValidationError("You cannot use 'me' as a username")
        return username


class AdminRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(default='user')

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'role', 'bio')


class TokenObtainSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']

    def validate_confirmation_code(self, code):
        if self.instance:
            if str(code) == str(self.instance.confirmation_code):
                return code
            else:
                raise ValidationError(
                    'Incorrect confirmation code. Try again.'
                )
        return code


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'role', 'bio')

    def validate_role(self, role):
        if role.lower() not in ROLES:
            raise ValidationError(f'Role must be one of: {ROLES}')
        user = self.context['request'].user
        if user.is_admin or user.is_moderator:
            return role
        return USER

    def validate_email(self, email):
        if (self.instance.email != email
                and User.objects.filter(email=email).count() > 0):
            raise ValidationError('A user with this email already exists.')

    def validate_username(self, username):
        if (self.instance.username != username
                and User.objects.filter(username=username).count() > 0):
            raise ValidationError('A user with this username already exists.')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов к тайтлам."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user
            ).exists():
                raise ValidationError(
                    'Можно добавить только'
                    'один отзыв на произведение'
                )
        return data


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    def get_rating(self, obj):
        average = obj.reviews.aggregate(Avg('score'))
        if not average['score__avg']:
            return None
        return int(average['score__avg'])


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title
