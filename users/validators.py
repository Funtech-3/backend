import re

from django.core.exceptions import ValidationError

from .constants import (NUMBER_ERROR_TEXT, REGEX_PHONE_NUMBER,
                        REGEX_TELEGRAM_USERNAME)


def validate_mobile(number):
    """Проверка соответствия вводимого номера - стандартам."""

    phone = re.compile(REGEX_PHONE_NUMBER)

    if not phone.search(number):
        raise ValidationError(NUMBER_ERROR_TEXT)
    return number


def validate_telegram(telegram_username):
    """Проверка вводимого телеграм никнейма в формате '@username'."""

    if not re.match(REGEX_TELEGRAM_USERNAME, telegram_username):
        raise ValidationError(
            "Некорректный формат никнейма в Telegram, используйте '@username'."
        )
