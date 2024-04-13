"""Модуль сериализаторов для приложения Tickets."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from tickets.models import Registration

User = get_user_model()


class UserTicketReadSerializer(serializers.ModelSerializer):
    """Сериализатор для Билетов."""

    name = serializers.CharField(read_only=True, source="event.title")
    city = serializers.CharField(read_only=True, source="event.city.name")
    date_event = serializers.CharField(read_only=True, source="event.date")

    class Meta:
        model = Registration
        fields = ("ticket_id", "city", "code", "name", "date_event")
