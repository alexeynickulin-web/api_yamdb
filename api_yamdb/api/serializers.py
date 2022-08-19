from rest_framework import serializers
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
