from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_STRING_FOR_USER,
    MAX_PHONE_NUMBER_LENGTH,
)
from .validators import validate_mobile, validate_telegram


class Tag(models.Model):
    """Модель тегов."""

    title = models.CharField(
        verbose_name="Название тега",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    """Модель пользователя для приложения."""
    USERNAME_FIELD = "yandex_id"
    yandex_id = models.PositiveBigIntegerField(
        verbose_name="Связанный Яндекс ID",
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        blank=True,
        null=True,
    )
    username = models.CharField(
        verbose_name="Логин из яндекс",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=MAX_LENGTH_EMAIL,
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=MAX_PHONE_NUMBER_LENGTH,
        blank=True,
        null=True,
        validators=(validate_mobile,),
    )
    telegram_username = models.CharField(
        verbose_name="Ник в телеграм",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        validators=(validate_telegram,),
        blank=True,
        null=True,
    )
    position = models.CharField(
        verbose_name="Должность",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        blank=True,
        null=True,
    )
    work_place = models.CharField(
        verbose_name="Место работы (компания)",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        verbose_name="Интересы",
        to=Tag,
        blank=True,
        related_name="users",
    )
    avatar = models.ImageField(
        verbose_name="Ссылка на фото",
        upload_to="users/images/",
        blank=True,
        null=True,
        default="https://avatars.yandex.net/get-yapic/<default_avatar_id>/",
    )

    class Meta:
        ordering = (
            "id",
            "username",
        )
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}"


class NotificationSwitch(models.Model):
    """Модель найстроек уведомлений."""

    user = models.OneToOneField(
        verbose_name="Пользователь",
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="user_notifications",
    )
    is_notification = models.BooleanField(
        verbose_name="Общий флаг активации уведомлений",
        default=False,
    )
    is_email = models.BooleanField(
        verbose_name="Уведомления по электронной почте",
        default=False,
    )
    is_telegram = models.BooleanField(
        verbose_name="Уведомления в телеграм",
        default=False,
    )
    is_phone = models.BooleanField(
        verbose_name="Уведомления по СМС",
        default=False,
    )
    is_push = models.BooleanField(
        verbose_name="Пуш уведомления",
        default=False,
    )

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
