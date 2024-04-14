"""Модуль административной команды создания суперпользователя."""

import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db.utils import IntegrityError

User = get_user_model()

ADMIN = {
    "yandex_id": 321,
    "username": "admin",
    "email": "admin@fake.up",
    "telegram_username": "@fake_admin_up",
    "last_name": "Pushkin",
    "first_name": "Aleksander",
    "phone_number": "+79001112233",
    "position": "Администратор",
    "work_place": "Umbrella corp.",
    "is_staff": True,
    "is_superuser": True,
}
PASSWORD = os.getenv("SUPERUSER_PASSWORD", "funtech_admin_12345")


class Command(BaseCommand):
    """Административная команда для создания суперпользователя
    с предустановленными параметрами.
    """

    help = "Создает суперпользователя с предустановленными параметрами."

    def make_admin(self):
        """Создать админа."""

        user, created = User.objects.get_or_create(**ADMIN)

        if user and created and PASSWORD:
            user.set_password(PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS("Суперпользователь создан."))
        else:
            self.stdout.write(
                self.style.ERROR(
                    "При создании суперпользователя возникли ошибки. "
                    "Пароль не установлен."
                )
            )

    def handle(self, *args, **options):
        """Исполнение административной команды."""

        try:
            self.make_admin()
        except IntegrityError as err:
            self.stdout.write(self.style.ERROR(f"ERROR - {err}"))
            exit()
        exit(0)