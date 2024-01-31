from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.is_admin or user.is_staff or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and (
            user.is_admin or user.is_staff or user.is_superuser
        )


class IsAthorModeraterAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return user.is_authenticated
        return user.is_authenticated and (
            user == obj.author
            or user.is_admin
            or user.is_moderator
            or user.is_staff
            or user.is_superuser
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
