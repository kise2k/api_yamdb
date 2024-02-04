from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return user.is_authenticated and user.is_admin


class IsAthorModeraterAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_moderator
                 or request.user == obj.author)
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS)


class AnonimReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user))
