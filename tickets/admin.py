"""Модуль настройки моделей приложения Ticket для административной панели."""

from django.contrib import admin

from .models import Registration, Ticket


class TicketInLine(admin.StackedInline):
    """Настройка вложенного отображения для модели Ticket."""
    model = Ticket


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Настройка отображения для модели"""
    inlines = [TicketInLine]
    list_display = (
        'event',
        'user',
        'status',
        'date_create',
    )
