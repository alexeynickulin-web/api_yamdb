from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import User, Comment, Review


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


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

    def validate_confirmation_code(self, data):
        if self.instance:
            if str(data) == str(self.instance.confirmation_code):
                return self.initial_data
            else:
                raise ValidationError(
                    'Incorrect confirmation code. Try again.'
                )
        return self.initial_data


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
        if role in ['user', 'admin', 'moderator']:
            if self.context['request'].user.role not in ['admin', 'moderator']:
                return 'user'
            return role
        raise ValidationError('Role must be user, admin or moderator.')

    def validate_email(self, email):
        if (self.instance.email != email and
                User.objects.filter(email=email).count() > 0):
            raise ValidationError('A user with this email already exists.')

    def validate_username(self, username):
        if (self.instance.username != username and
                User.objects.filter(username=username).count() > 0):
            raise ValidationError('A user with this username already exists.')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
