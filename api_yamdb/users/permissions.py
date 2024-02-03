from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_staff or user.is_superuser or user.is_admin
        )


class IsAthorModeraterAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            request.method in permissions.SAFE_METHODS
            or user.is_authenticated
            and (request.user
                 or user.is_admin
                 or user.is_staff
                 or user.is_superuser)
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
