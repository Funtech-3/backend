import re

from django.core.exceptions import ValidationError

from .constants import (
    NUMBER_ERROR_TEXT,
    REGEX_PHONE_NUMBER,
    USERNAME_ERROR_TEXT,
)


def validate_username(username):
    """Проверка на выбор username отличного от me."""

    if username.lower() == "me":
        raise ValidationError(USERNAME_ERROR_TEXT)
    return username


def validate_mobile(number):
    "Проверка соответствия вводимого номера - стандартам."

    phone = re.compile(REGEX_PHONE_NUMBER)

    if not phone.search(number):
        raise ValidationError(NUMBER_ERROR_TEXT)
    return number
