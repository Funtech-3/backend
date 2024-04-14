"""Модуль утилит отправки уведомлений по электронной почте."""

from datetime import datetime
from email.mime.image import MIMEImage
from io import BytesIO

import qrcode
from django.conf import settings
from django.core.mail import EmailMessage
from tickets.constants import (
    QR_CODE_CONTENT_ID,
    TICKET_CHECK_URL_TEMPLATE,
    TICKET_LETTER_SUBJECT,
    TICKET_LETTER_TEMPLATE,
)
from tickets.models import Registration


def make_qr_code_image_data(data_to_encode: str) -> bytes:
    """Создает изображение QR-кода.
    Возвращает массив байт изображения."""
    qr_image = qrcode.make(data_to_encode)
    byte_array = BytesIO()
    qr_image.save(byte_array)
    byte_array_value = byte_array.getvalue()
    return byte_array_value


def prepare_MIME_image_for_email(image: bytes) -> MIMEImage:
    """Возвращает MIMEImage объект из данных изображения,
    устанавливает заголовок объекта для письма."""
    mime_image = MIMEImage(image)
    mime_image.add_header("Content-ID", f"<{QR_CODE_CONTENT_ID}>")
    return mime_image


def extract_ticket_info(ticket: Registration) -> dict:
    """Извлекает данные из моделей о событие и регистрации для отправки,
    билета."""
    result = dict(
        event_name=ticket.event.title,
        event_type=ticket.event.type,
        city=ticket.event.city.name,
        event_date=datetime.strftime(
            ticket.event.date,
            settings.REST_FRAMEWORK.get("DATE_FORMAT", "%d.%m.%Y"),
        ),
        recipient=ticket.user.email,
        code=ticket.code,
    )
    return result


def prepare_letter_body(ticket_info: dict) -> str:
    """ПОдготовка тела письма."""
    body = TICKET_LETTER_TEMPLATE.format(
        ticket_info.get("event_type"),
        ticket_info.get("event_name"),
        ticket_info.get("city"),
        ticket_info.get("event_date"),
        QR_CODE_CONTENT_ID,
    )
    return body


def send_ticket_info(ticket: Registration):
    """Отправляет письмо по электронной почте с информацией
    о регистрации на событие и qr-кодом."""
    ticket_info = extract_ticket_info(ticket=ticket)
    letter: EmailMessage = EmailMessage(
        subject=TICKET_LETTER_SUBJECT,
        from_email=settings.EMAIL_HOST_USER,
        body=prepare_letter_body(ticket_info=ticket_info),
        to=(
            settings.EMAIL_HOST_USER,
            ticket_info.get("recipient"),
        ),
    )
    letter.content_subtype = "html"
    letter.attach(
        prepare_MIME_image_for_email(
            make_qr_code_image_data(
                TICKET_CHECK_URL_TEMPLATE.format(ticket_info.get("code"))
            )
        )
    )
    letter.send(fail_silently=False)
