"""Модуль вьюсетов для билетов и регистрации."""

from rest_framework import mixins, viewsets


class RetrieveDestroyViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет на чтение, удаление."""

    pass


class RetrieveViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет на чтение."""

    pass
