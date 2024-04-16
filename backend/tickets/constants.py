"""Модуль констант для приложения tickets."""

STATUS_MAX_LENGTH = 25
TICKET_CODE_LENGTH = 36

# Для модуля email_utils.py
QR_CODE_CONTENT_ID = "qrcode"
TICKET_LETTER_TEMPLATE = (
    "<HTML><BODY>"
    "<h1>Ваш билет</h1>"
    "<h2>{}</h2>"
    "<h3>{}</h3>"
    "<h2>{}</h2>"
    "<h3>{}</h3>"
    '<img src="cid:{}">'
    "</BODY></HTML>"
)
TICKET_LETTER_SUBJECT = "Ваш билет"
TICKET_CHECK_URL_TEMPLATE = (
    "https://funtech.myddns.me/api/v1/user/ticket_check/{}/"
)
