MAX_PHONE_NUMBER_LENGTH = 12
MAX_LENGTH_STRING_FOR_USER = 150
MAX_LENGTH_EMAIL = 254
REGEX_CHAR_USERNAME = r"^[\w.@+-]+$"
REGEX_ERROR_TEXT = "Имя пользователя содержит недопустимые символы."

REGEX_PHONE_NUMBER = r"^\+?[7-8]?[0-9]{10}$"
NUMBER_ERROR_TEXT = (
    "Неверный мобильный номер. Введите номер без '-',"
    "используйте только цифры и '+'."
)
USERNAME_ERROR_TEXT = "Выберите другое имя пользователя, не используйте 'me'"

LIMIT_POSTS_PER_PAGE = 15
