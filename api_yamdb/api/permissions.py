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
