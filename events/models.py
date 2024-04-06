from django.contrib.auth import get_user_model
from django.db import models

from .constants import (
    EVENT_MODES,
    EVENT_REGISTRATION_STATUSES,
    MAX_CITY_NAME,
    MAX_EVENT_ADDRESS,
    MAX_EVENT_MODE,
    MAX_EVENT_REG_STATUS,
    MAX_EVENT_SLUG,
    MAX_EVENT_TITLE,
    MAX_FIRST_NAME,
    MAX_LAST_NAME,
    MAX_POSITION,
    MAX_STEP_TITLE,
    MAX_TAG_TITLE,
    MAX_WORK_PLACE,
)


User = get_user_model()


class City(models.Model):
    """Модель городов."""
    name = models.CharField(
        verbose_name="Название города",
        max_length=MAX_CITY_NAME,
        unique=True
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "города"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""
    title = models.CharField(
        verbose_name="Название тега",
        max_length=MAX_TAG_TITLE,
        unique=True
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.title


class Speaker(models.Model):
    """Модель спикеров."""
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_FIRST_NAME
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_LAST_NAME
    )
    work_place = models.CharField(
        verbose_name="Место работы",
        max_length=MAX_WORK_PLACE
    )
    position = models.CharField(
        verbose_name="Должность",
        max_length=MAX_POSITION
    )
    image = models.ImageField(
        verbose_name="Фото",
        upload_to="speakers",
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
    title = models.CharField(
        verbose_name="Название",
        max_length=MAX_EVENT_TITLE
    )
    description = models.TextField(verbose_name="Описание")
    slug = models.CharField(
        verbose_name="Символьный код",
        max_length=MAX_EVENT_SLUG,
        unique=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name="Город проведения"
    )
    address = models.CharField(
        verbose_name="Адрес",
        max_length=MAX_EVENT_ADDRESS
    )
    date = models.DateField(verbose_name="Дата проведения", null=True)
    registration_status = models.CharField(
        verbose_name="Статус регистрации",
        max_length=MAX_EVENT_REG_STATUS,
        choices=EVENT_REGISTRATION_STATUSES
    )
    tags = models.ManyToManyField(Tag)
    mode = models.CharField(
        verbose_name="Формат проведения",
        max_length=MAX_EVENT_MODE,
        choices=EVENT_MODES
    )
    image = models.ImageField(verbose_name="Фото", upload_to="events")
    favorited_by = models.ManyToManyField(
        User,
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
        max_length=MAX_STEP_TITLE
    )
    start_time = models.TimeField(verbose_name="Начало этапа")
    description = models.TextField(verbose_name="Описание", blank=True)
    speakers = models.ManyToManyField(
        Speaker,
        blank=True,
        verbose_name="Спикер",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name="Событие"
    )

    class Meta:
        verbose_name = "Этап события"
        verbose_name_plural = "этапы события"
        ordering = ('start_time',)

    def __str__(self):
        return self.title
