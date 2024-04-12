from rest_framework import permissions


class IsAuthenticatedAndOwner(permissions.BasePermission):
    """Пермишен для владельца ЛК, на изменение и просмотр своих данных."""

    def has_permission(self, request, view):
        if request.method in ["POST", "DELETE"]:
            return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
