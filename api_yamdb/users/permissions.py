from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_admin or user.is_staff or user.is_superuser
        )


class IsAthorModeraterAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        return (
            request.method in permissions.SAFE_METHODS
            or user.is_authenticated
            and (obj.author == request.user
                 or user.is_admin
                 or user.is_moderator
                 or user.is_staff
                 or user.is_superuser)
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
