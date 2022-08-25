from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'moderator':
            return True
        return False


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (IsAuthor().has_object_permission(request, view, obj)
                or
                IsModerator().has_object_permission(request, view, obj)
                or
                IsAdminOrSuperuser.has_object_permission(request, view, obj)
                )


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Проверка на автора, админа или модератора."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_authenticated and request.user.role == 'moderator'
            or request.user.is_authenticated and obj.author == request.user
            or request.user.is_authenticated and request.method == 'POST'
        )
