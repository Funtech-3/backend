"""Модуль разрешений для представлений приложения Api."""

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsOwner(BasePermission):
    """Разрешен доступ на уровне объекта только владельце регистрации.

    В остальные случаях разрешены безопасные методы HTTP: GET, HEAD, OPTIONS.
    """

    def has_object_permission(self, request, view, obj):
        """Ограничение на уровне объекта."""

        return obj.user == request.user
