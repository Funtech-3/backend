"""Модуль моделей приложения tickets."""

import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from events.models import Event
from .constants import STATUS_MAX_LENGTH

User = get_user_model()


class Ticket(models.Model):
    """Модель Билет."""
    qr_code = models.ImageField(verbose_name="QR-код", upload_to='qr_codes')
    code = models.UUIDField(
        verbose_name="Уникальный код",
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Уникальный код для кодирования данных о билете в QR-код.",
    )

    def __str__(self):
        return self.code

    class Meta:
        """Класс настроек модели Ticket."""
        verbose_name = "Билет"
        verbose_name_plural = "билеты"


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
        related_name='registrations',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Участник",
        related_name='registrations',
    )
    status = models.CharField(
        choices=Status,
        max_length=STATUS_MAX_LENGTH,
        verbose_name="Статус регистрации",
        related_name='статусы регистрации',
    )
    date_create = models.DateField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
        related_name='даты регистрации',
    )
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="registrations"
    )

    class Meta:
        """Класс настроек модели Registration."""
        verbose_name = "Регистрация"
        verbose_name_plural = "регистрации"
