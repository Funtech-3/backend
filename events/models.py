from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Tag
from .constants import (
    MAX_CHAR_FOR_EVENTS,
    MAX_EVENT_MODE,
    MAX_EVENT_REG_STATUS,
    MAX_LONG_CHAR_FOR_EVENTS
)

User = get_user_model()


class City(models.Model):
    """Модель городов."""
    name = models.CharField(
        verbose_name="Название города",
        max_length=MAX_CHAR_FOR_EVENTS,
        unique=True
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.name


class EventType(models.Model):
    """Модель типов событий."""
    title = models.CharField(
        verbose_name="Название типа",
        max_length=MAX_CHAR_FOR_EVENTS,
        unique=True
    )

    class Meta:
        verbose_name = "Тип события"
        verbose_name_plural = "типы событий"

    def __str__(self):
        return self.title


class Speaker(models.Model):
    """Модель спикеров."""
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_CHAR_FOR_EVENTS
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_CHAR_FOR_EVENTS
    )
    work_place = models.CharField(
        verbose_name="Место работы",
        max_length=MAX_LONG_CHAR_FOR_EVENTS
    )
    position = models.CharField(
        verbose_name="Должность",
        max_length=MAX_LONG_CHAR_FOR_EVENTS
    )
    image = models.ImageField(
        verbose_name="Фото",
        upload_to="events/images/speakers",
        blank=True
    )

    class Meta:
        verbose_name = "Спикер"
        verbose_name_plural = "спикеры"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}"


class Event(models.Model):
    """Модель событий."""

    class RegistrationStatus(models.TextChoices):
        OPEN = "OPEN", _("Регистрация открыта")
        CLOSED = "CLOSED", _("Регистрация завершена")
        PENDING = "PENDING", _("Ожидание регистрации")

    class EventMode(models.TextChoices):
        ONLINE = "ONLINE", _("Онлайн")
        OFFLINE = "OFFLINE", _("Офлайн")

    title = models.CharField(
        verbose_name="Название",
        max_length=MAX_CHAR_FOR_EVENTS
    )
    description = models.TextField(verbose_name="Описание")
    slug = models.CharField(
        verbose_name="Символьный код",
        max_length=MAX_CHAR_FOR_EVENTS,
        unique=True
    )
    city = models.ForeignKey(
        to=City,
        on_delete=models.PROTECT,
        verbose_name="Город проведения"
    )
    address = models.CharField(
        verbose_name="Адрес",
        max_length=MAX_CHAR_FOR_EVENTS
    )
    date = models.DateField(verbose_name="Дата проведения", null=True)
    registration_status = models.CharField(
        verbose_name="Статус регистрации",
        max_length=MAX_EVENT_REG_STATUS,
        choices=RegistrationStatus.choices,
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name="Теги"
    )
    mode = models.CharField(
        verbose_name="Формат проведения",
        max_length=MAX_EVENT_MODE,
        choices=EventMode.choices
    )
    type = models.ForeignKey(
        to=EventType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    preview_image = models.ImageField(
        verbose_name="Превью-фото события",
        upload_to="events/images/event/preview",
        blank=True,
        null=True
    )
    image = models.ImageField(
        verbose_name="Фото для страницы события",
        upload_to="events/images/event/detail",
    )
    favorited_by = models.ManyToManyField(
        to=User,
        blank=True,
        related_name="favorite_events",
        verbose_name="Добавили в избранное"
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "события"
        default_related_name = "events"
        ordering = ("-date", "title")

    def __str__(self):
        return self.title


class EventStep(models.Model):
    """Модель этапов события."""
    title = models.CharField(
        verbose_name="Название",
        max_length=MAX_LONG_CHAR_FOR_EVENTS
    )
    start_time = models.TimeField(verbose_name="Начало этапа")
    description = models.TextField(verbose_name="Описание", blank=True)
    speakers = models.ManyToManyField(
        to=Speaker,
        blank=True,
        verbose_name="Спикеры",
    )
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        verbose_name="Событие"
    )

    class Meta:
        verbose_name = "Этап события"
        verbose_name_plural = "этапы события"
        default_related_name = "steps"
        ordering = ('start_time',)

    def __str__(self):
        return self.title
