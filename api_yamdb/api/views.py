import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import IsAdminOrSuperuser, IsAuthorOrAdminOrModerator
from .serializers import (AdminRegistrationSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          TokenObtainSerializer, UserSerializer)


class RegistrationViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = secrets.token_urlsafe(nbytes=10)
        send_mail(subject='Confirmation Code for Yamdb',
                  message=code, from_email=settings.ADMIN_EMAIL,
                  recipient_list=[self.request.data['email']])
        serializer.save(confirmation_code=code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainViewset(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def update(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User,
                                 username=serializer.
                                 validated_data['username'])
        token = RefreshToken.for_user(user)
        return Response({"token": str(token.access_token)},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsAdminOrSuperuser, )
    filter_backends = [SearchFilter]
    search_fields = ['username']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated], url_path='me')
    def get_or_update_current_user(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(request.user, '_prefetched_objects_cache', None):
                request.user._prefetched_objects_cache = {}
            return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments_review.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name',)
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser, ]

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return super().get_permissions()


class GenreViewSet(CreateListDestroyViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name',)
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser, ]

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=models.Avg('reviews__score')
    )
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser, ]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return super().get_permissions()
