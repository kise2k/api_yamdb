from rest_framework import permissions
from django.http import HttpResponseNotAllowed


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
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class AnonimReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS