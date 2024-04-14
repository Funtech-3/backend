"""Модуль настройки моделей приложения Ticket для административной панели."""

from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Настройка отображения для модели Registration."""

    list_display = (
        "event",
        "user",
        "status",
        "date_create",
        "ticket_code_verbose",
        "ticket_id_verbose",
    )
    list_editable = ("status",)

    @admin.display(description="Код билета")
    def ticket_code_verbose(self, object: Registration):
        """Строковое свойство для кода билета."""
        if object.status == Registration.Status.CONFIRMED:
            return object.ticket_code
        return "-"

    @admin.display(description="ИД Билета")
    def ticket_id_verbose(self, object: Registration):
        """Строковое свойство для ticket_id."""
        if object.status == Registration.Status.CONFIRMED:
            return object.ticket_id
        return "-"