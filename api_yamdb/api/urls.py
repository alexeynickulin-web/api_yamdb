from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (CommentViewSet, ReviewViewSet)

from .views import (CurrentUserViewSet, DeleteUserViewSet, RegistrationViewSet,
                    TokenObtainViewset, UsersViewSet)

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='User')
router.register(r'auth/signup', RegistrationViewSet, basename='User')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/users/me/', CurrentUserViewSet.as_view(actions={
        'get': 'retrieve',
        'patch': 'update',
    }
    )),
    path('v1/users/me/<str:username>/', DeleteUserViewSet.as_view(actions={
        'delete': 'destroy'
    })),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenObtainViewset.as_view(
        actions={'post': 'update'}))
]
