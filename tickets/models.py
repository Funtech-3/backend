"""Модуль моделей приложения tickets."""

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from events.models import Event

from .constants import STATUS_MAX_LENGTH, TICKET_CODE_LENGTH
from .utils import get_uuid_str

User = get_user_model()


class Registration(models.Model):
    """Модель регистрация на события."""

    class Status(models.TextChoices):
        """Перечисление статусов регистрации."""

        PENDING = "PENDING", _("Ожидание подтверждения")
        REJECTED = "REJECTED", _("Заявка отклонена")
        CONFIRMED = "CONFIRMED", _("Вы участвуете")

    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        verbose_name="Событие",
        unique=False,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Участник",
        unique=False,
    )
    status = models.CharField(
        choices=Status,
        max_length=STATUS_MAX_LENGTH,
        verbose_name="Статус регистрации",
        default=Status.PENDING,
    )
    date_create = models.DateField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
    )
    ticket_code = models.CharField(
        verbose_name="Уникальный код",
        default=get_uuid_str,
        auto_created=True,
        unique=True,
        max_length=TICKET_CODE_LENGTH,
        help_text="Уникальный код для кодирования данных о билете в QR-код.",
    )

    class Meta:
        """Класс настроек модели Registration."""

        verbose_name = "Регистрация"
        verbose_name_plural = "регистрации"
        default_related_name = "ticket_registrations"
        constraints = [
            UniqueConstraint(
                fields=[
                    'user',
                    'event',
                ],
                name='Unique_event_for_each_user',
            )
        ]

    def ___str__(self):
        """Строковое представление модели Регистрация."""
        return f"{self.date_create} - {self.status}"

    @property
    def code(self):
        """Показывает код билета только если регистрация подтверждена,
        иначе пустая строка."""
        if self.status == Registration.Status.CONFIRMED:
            return self.ticket_code
        return ""

    @property
    def ticket_id(self):
        """Показывает ticket_id код билета только если регистрация
        подтверждена, иначе None."""
        if self.status == Registration.Status.CONFIRMED:
            return self.pk
        return None
