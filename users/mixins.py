"""Модуль вьюсетов для билетов и регистрации."""

from rest_framework import mixins, viewsets


class RetrieveUpdateViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет на чтение, обновление."""

    pass
