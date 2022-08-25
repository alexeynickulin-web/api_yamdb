import secrets
from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)
from rest_framework import mixins, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User, Comment

from .permissions import (IsAdminOrSuperuser, IsAuthorOrAdminOrModerator)
from .serializers import (AdminRegistrationSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          RegistrationSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          TokenObtainSerializer, UserSerializer)


class RegistrationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)

    def perform_create(self, serializer):
        code = secrets.token_urlsafe(nbytes=10)
        send_mail(subject='Confirmation Code for Yamdb',
                  message=code, from_email='registration@yamdb.com',
                  recipient_list=[self.request.data['email']])
        serializer.save(confirmation_code=code)


class TokenObtainViewset(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def update(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'username' in self.request.data:
            user = get_object_or_404(User, username=request.data["username"])
            serializer = TokenObtainSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            token = RefreshToken.for_user(user)
            return Response({"token": str(token.access_token)},
                            status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrSuperuser, )
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminRegistrationSerializer
        return UserSerializer


class CurrentUserViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class DeleteUserViewSet(mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser, ]
    lookup_field = 'username'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if self.request.user.reviews.filter(title=title_id).exists():
            raise ValidationError('К этому произведению уже оставлен отзыв.')
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            review_id=self.kwargs.get('review_id')
        )
        return queryset

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        if get_object_or_404(Review, id=self.kwargs.get('review_id')):
            serializer.save(
                author=self.request.user,
                review_id=self.kwargs.get('review_id')
            )


class CategoryViewSet(viewsets.ModelViewSet):
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


class DeleteCategoryViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminOrSuperuser]
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]


class GenreViewSet(viewsets.ModelViewSet):
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


class DeleteGenreViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminOrSuperuser]
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='contains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
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
