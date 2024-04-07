from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_STRING_FOR_USER,
    MAX_PHONE_NUMBER_LENGTH,
    REGEX_CHAR_USERNAME,
    REGEX_ERROR_TEXT,
)
from .validators import validate_mobile, validate_username


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


class Notifications(models.Model):
    """Модель найстроек уведомлений."""

    notification = models.BooleanField(
        verbose_name="Общий флаг активации уведомлений",
        default=False,
    )
    email_notification = models.BooleanField(
        verbose_name="Уведомления по электронной почте",
        default=False,
    )
    telegram_notification = models.BooleanField(
        verbose_name="Уведомления в телеграм",
        default=False,
    )
    phone_notification = models.BooleanField(
        verbose_name="Уведомления по СМС",
        default=False,
    )
    push_notification = models.BooleanField(
        verbose_name="Пуш уведомления",
        default=False,
    )

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"


class CustomUser(AbstractUser):
    """Модель пользователя для приложения."""

    first_name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    username = models.CharField(
        verbose_name="Уникальный юзернейм",
        max_length=MAX_LENGTH_STRING_FOR_USER,
        unique=True,
        validators=(
            RegexValidator(
                regex=REGEX_CHAR_USERNAME,
                message=_(REGEX_ERROR_TEXT),
            ),
            validate_username,
        ),
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        validators=(validate_email,),
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=MAX_PHONE_NUMBER_LENGTH,
        unique=True,
        validators=(validate_mobile,),
    )
    telegram_username = models.CharField(
        verbose_name="Ник в телеграм",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    position = models.CharField(
        verbose_name="Должность",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    work_place = models.CharField(
        verbose_name="Место работы(компания)",
        max_length=MAX_LENGTH_STRING_FOR_USER,
    )
    tags = models.ForeignKey(
        verbose_name="Интересы",
        to=Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_tags",
    )
    notifications = models.ForeignKey(
        verbose_name="Настройки уведомлений",
        to=Notifications,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="user_notifications",
    )
    yandex_id = models.PositiveBigIntegerField(
        verbose_name="Связанный Яндекс ID",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=("username", "email"),
                name="unique_user_with_email",
            ),
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}"
