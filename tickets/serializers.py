"""Модуль сериализаторов для приложения Tickets."""


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from tickets.models import Registration


User = get_user_model()

# from users.serializers import DjoserUserSerializer


class UserTicketReadSerializer(serializers.ModelSerializer):
    """Сериализатор для Билетов."""
    name = serializers.CharField(read_only=True, source="event.title")
    city = serializers.CharField(read_only=True, source="event.city.name")
    date_event = serializers.CharField(read_only=True, source="event.date")

    class Meta:
        model = Registration
        fields = ('ticket_id', 'city', 'code', 'name', 'date_event')


class UserTicketDestroySerializer(serializers.ModelSerializer):
    """Сериализатор для Билетов."""

    class Meta:
        model = Registration
        fields = ('id')
