from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, DeleteCategoryViewSet,
                    DeleteGenreViewSet, GenreViewSet, RegistrationViewSet,
                    ReviewViewSet, TitleViewSet, TokenObtainViewset,
                    UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='User')
router.register(r'auth/signup', RegistrationViewSet, basename='User')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path(
        'v1/categories/<str:slug>/',
        DeleteCategoryViewSet.as_view(actions={'delete': 'destroy'})),
    path(
        'v1/genres/<str:slug>/',
        DeleteGenreViewSet.as_view(actions={'delete': 'destroy'})),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenObtainViewset.as_view(
        actions={'post': 'update'}))
]
