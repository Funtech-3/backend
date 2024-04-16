"""Модуль утилит для приложения Ticket."""

import uuid


def get_uuid_str() -> str:
    """Получить строку с UUID кодом."""
    return str(uuid.uuid4())
