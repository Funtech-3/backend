import re

from django.core.exceptions import ValidationError

from .constants import (
    INVALID_USERNAME,
    NUMBER_ERROR_TEXT,
    REGEX_CHAR_USERNAME,
    REGEX_PHONE_NUMBER,
    REGEX_TELEGRAM_USERNAME,
)


def validate_username(username):
    """
    Проверка на выбор username отличного от me
    и соответствие регулярным символам.
    """

    if username in INVALID_USERNAME:
        raise ValidationError(f"Нельзя использовать {username} как 'username'")
    invalid_symbols = re.sub(REGEX_CHAR_USERNAME, "", username)
    if invalid_symbols:
        raise ValidationError(
            f"Нельзя использовать символы {''.join(set(invalid_symbols))}"
        )
    return username


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
