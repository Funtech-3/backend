"""Модуль настройки приложения Tickets."""

from django.apps import AppConfig


class TicketsConfig(AppConfig):
    """Класс настройки приложения Tickets."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'
    verbose_name = 'Регистрация билетов'
