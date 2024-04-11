"""Модуль представлений для приложения Ticket."""

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from tickets.models import Registration
from tickets.serializers import UserTicketReadSerializer, UserTicketDestroySerializer
from tickets.mixins import RetrieveDestroyViewSet, CreateRetrieveViewSet

User = get_user_model()


class UserTicketViewSet(RetrieveDestroyViewSet):
    """Вьюсет для Билетов."""

    queryset = Registration.objects.filter(status=Registration.Status.CONFIRMED).all()
    serializer_class = UserTicketReadSerializer


    def get_serializer_class(self):
        """Возвражает класс-сериализатор в зависимости от метода запроса."""

        if self.request.method in SAFE_METHODS:
            return UserTicketReadSerializer
        elif self.request.method == 'DELETE':
            return UserTicketDestroySerializer
        return UserTicketDestroySerializer
    

class EventRegistrationVieSet(CreateRetrieveViewSet):
    """Вьюсет регистрации билета."""
    pass