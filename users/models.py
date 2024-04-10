from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models

from .constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_STRING_FOR_USER,
    MAX_PHONE_NUMBER_LENGTH,
)
<<<<<<< Updated upstream
from .validators import validate_mobile, validate_telegram, validate_username
=======
from .validators import validate_mobile, validate_telegram
>>>>>>> Stashed changes


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


<<<<<<< Updated upstream
=======
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
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=MAX_LENGTH_EMAIL,
        blank=True,
        null=True,
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


>>>>>>> Stashed changes
class NotificationSwitch(models.Model):
    """Модель найстроек уведомлений."""

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
        validators=(validate_username,),
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
        validators=(validate_telegram,),
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
        to=NotificationSwitch,
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
    avatar = models.ImageField(
        verbose_name="Ссылка на фото",
        upload_to="users/images/",
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
