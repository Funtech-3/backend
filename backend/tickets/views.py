"""Модуль представлений для приложения Ticket."""

from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from tickets.mixins import RetrieveDestroyViewSet
from tickets.models import Registration
from tickets.permissions import IsOwner
from tickets.serializers import UserTicketReadSerializer

User = get_user_model()


class UserTicketViewSet(RetrieveDestroyViewSet):
    """Вьюсет для чтения и удаления Билетов."""

    queryset = Registration.objects.filter(
        status=Registration.Status.CONFIRMED
    ).all()
    serializer_class = UserTicketReadSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
    pagination_class = None

    def get_serializer_class(self):
        """Возвращает класс-сериализатор в зависимости от метода запроса."""
        if self.request.method in SAFE_METHODS:
            return UserTicketReadSerializer
        super().get_serializer_class()