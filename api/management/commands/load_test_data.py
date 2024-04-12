"""Модуль административной команды загрузки тестовых данных."""

import datetime
import os
from csv import DictReader
from random import randint

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from events.models import City, Event, EventStep, EventType, Speaker, Tag
from tickets.models import Registration
from users.models import NotificationSwitch

User = get_user_model()

TEST_DATA_DIR_NAME = "test_data"
TEST_DATA_PATH = os.path.join(os.getcwd(), TEST_DATA_DIR_NAME)
MESSAGE = "был успешно загружен в базу данных."
UTF = "UTF-8"

TAGS_CSV = os.path.join(TEST_DATA_PATH, "tags_data.csv")
CITY_CSV = os.path.join(TEST_DATA_PATH, "city_data.csv")
EVENT_TYPE_CSV = os.path.join(TEST_DATA_PATH, "event_type_data.csv")

SPEAKER_CSV = os.path.join(TEST_DATA_PATH, "speaker_data.csv")
SPEAKER_IMAGE_PATH = os.path.join(TEST_DATA_PATH, "images", "speakers")
SPEAKER_IMAGES = {
    1: "1.jpeg",
    2: "2.jpg",
    3: "3.png",
    4: "4.jpg",
    5: "5.jpg",
    6: "6.jpg",
    7: "7.jpg",
}

USER_IMAGES = {
    1: "cat.png",
    2: "enot.png",
    3: "fox.jpg",
}
USERS_CSV = os.path.join(TEST_DATA_PATH, "users_data.csv")
USER_IMAGE_PATH = os.path.join(TEST_DATA_PATH, "images", "avatars")
USERS_TAGS_CSV = os.path.join(TEST_DATA_PATH, "users_tags_data.csv")
USERS_CITIES_CSV = os.path.join(TEST_DATA_PATH, "users_cities_data.csv")
NOTIFICATION_CSV = os.path.join(TEST_DATA_PATH, "notification_data.csv")
EVENT_CSV = os.path.join(TEST_DATA_PATH, "events_data.csv")
EVENT_TAG_CSV = os.path.join(TEST_DATA_PATH, "event_tag_data.csv")

EVENT_PREVIEW_IMAGES = {
    1: "1.png",
    2: "2.png",
    3: "3.png",
    4: "4.png",
}

EVENT_FULL_IMAGES = {
    1: "1_f.png",
    2: "2_f.png",
    3: "3_f.png",
    4: "4_f.png",
}

EVENT_IMAGE_PATH = os.path.join(TEST_DATA_PATH, "images", "events")

EVENT_STEPS_CSV = os.path.join(TEST_DATA_PATH, "event_step_data.csv")
EVENT_STEPS_SPEAKERS_MESSAGE = "event_step_speakers_data random"
REGISTRATION_CSV = os.path.join(TEST_DATA_PATH, "registration_data.csv")
EVENT_FAVORITE_CSV = os.path.join(TEST_DATA_PATH, "event_favorited_data.csv")


class Command(BaseCommand):
    """Административная команда для загрузки тестовых данных."""

    help = (
        "Загружает тестовые данные из csv файлов и изображения в базу "
        "данных проекта. До их загрузки должен быть создан один "
        "пользователь."
    )

    def load_tags(self):
        """Загрузка тегов."""

        for row in DictReader(f=open(TAGS_CSV, encoding=UTF)):
            Tag.objects.update_or_create(**row)
        self.stdout.write(self.style.SUCCESS(f"{TAGS_CSV} {MESSAGE}"))

    def load_city(self):
        """Загрузка городов."""

        for row in DictReader(f=open(CITY_CSV, encoding=UTF)):
            City.objects.update_or_create(**row)
        self.stdout.write(self.style.SUCCESS(f"{CITY_CSV} {MESSAGE}"))

    def load_event_type(self):
        """Загрузка типов ивентов."""

        for row in DictReader(f=open(EVENT_TYPE_CSV, encoding=UTF)):
            EventType.objects.update_or_create(**row)
        self.stdout.write(self.style.SUCCESS(f"{EVENT_TYPE_CSV} {MESSAGE}"))

    def load_speaker(self):
        """Загрузка городов."""
        counter = 0
        for row in DictReader(f=open(SPEAKER_CSV, encoding=UTF)):
            counter += 1
            object, created = Speaker.objects.update_or_create(**row)
            f = open(
                os.path.join(SPEAKER_IMAGE_PATH, SPEAKER_IMAGES.get(counter)),
                # f'{SPEAKER_IMAGE_PATH}{SPEAKER_IMAGES.get(counter)}',
                mode="rb",
            )
            image_file = File(f)
            object.image.save(
                SPEAKER_IMAGES.get(counter), image_file, save=True
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{os.path.join(SPEAKER_IMAGE_PATH, SPEAKER_IMAGES.get(counter))} {MESSAGE}"
                )
            )
        self.stdout.write(self.style.SUCCESS(f"{SPEAKER_CSV} {MESSAGE}"))

    def load_users(self):
        """Загрузка пользователей."""
        counter = 0
        for row in DictReader(f=open(USERS_CSV, encoding=UTF)):
            counter += 1
            object, created = User.objects.update_or_create(**row)
            f = open(
                os.path.join(USER_IMAGE_PATH, USER_IMAGES.get(counter)),
                mode="rb",
            )
            image_file = File(f)
            object.avatar.save(USER_IMAGES.get(counter), image_file, save=True)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{os.path.join(USER_IMAGE_PATH, USER_IMAGES.get(counter))} {MESSAGE}"
                )
            )
        self.stdout.write(self.style.SUCCESS(f"{USERS_CSV} {MESSAGE}"))

    def load_users_tags(self):
        """Загрузка тегов пользователя."""

        for row in DictReader(f=open(USERS_TAGS_CSV, encoding=UTF)):
            user_object = User.objects.get(pk=row.get("user_id"))
            tag = Tag.objects.get(pk=row.get("tag_id"))
            user_object.tags.add(tag)
            user_object.save()
        self.stdout.write(self.style.SUCCESS(f"{USERS_TAGS_CSV} {MESSAGE}"))

    def load_users_cities(self):
        """Загрузка тегов пользователя."""

        for row in DictReader(f=open(USERS_CITIES_CSV, encoding=UTF)):
            user = User.objects.get(pk=row.get("user_id"))
            city = City.objects.get(pk=row.get("city_id"))
            user.cities.add(city)
            user.save()
        self.stdout.write(self.style.SUCCESS(f"{USERS_CITIES_CSV} {MESSAGE}"))

    def load_users_notifications(self):
        """Загрузка NOTIFICATION NotificationSwitch."""

        for row in DictReader(f=open(NOTIFICATION_CSV, encoding=UTF)):
            user_id = row.pop("user_id")
            user_object = User.objects.get(pk=user_id)
            NotificationSwitch.objects.update_or_create(
                user=user_object, **row
            )
        self.stdout.write(self.style.SUCCESS(f"{NOTIFICATION_CSV} {MESSAGE}"))

    def load_event(self):
        """Загрузка Event."""

        counter = 0
        for row in DictReader(f=open(EVENT_CSV, encoding=UTF)):
            counter += 1
            event_date = datetime.datetime.strptime(
                row.pop("date"), "%Y-%m-%d"
            )
            event_type = EventType.objects.get(pk=row.pop("type_id"))
            city = City.objects.get(pk=row.pop("city_id"))
            event_object, created = Event.objects.get_or_create(
                type=event_type,
                date=event_date,
                city=city,
                **row,
            )

            f = open(
                os.path.join(
                    EVENT_IMAGE_PATH, EVENT_PREVIEW_IMAGES.get(counter)
                ),
                mode="rb",
            )
            preview_image_file = File(f)
            event_object.preview_image.save(
                EVENT_PREVIEW_IMAGES.get(counter),
                preview_image_file,
                save=True,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{os.path.join(EVENT_IMAGE_PATH, EVENT_PREVIEW_IMAGES.get(counter))} {MESSAGE}"
                )
            )

            f = open(
                os.path.join(EVENT_IMAGE_PATH, EVENT_FULL_IMAGES.get(counter)),
                mode="rb",
            )
            full_image_file = File(f)
            event_object.image.save(
                EVENT_FULL_IMAGES.get(counter), full_image_file, save=True
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{os.path.join(EVENT_IMAGE_PATH, EVENT_FULL_IMAGES.get(counter))} {MESSAGE}"
                )
            )
            event_object.save()

        self.stdout.write(self.style.SUCCESS(f"{EVENT_CSV} {MESSAGE}"))

    def load_event_tags(self):
        """Загрузка тегов."""

        for row in DictReader(f=open(EVENT_TAG_CSV, encoding=UTF)):
            event_object = Event.objects.get(pk=row.get("event_id"))
            tag = Tag.objects.get(pk=row.get("tag_id"))
            event_object.tags.add(tag)
            event_object.save()

        self.stdout.write(self.style.SUCCESS(f"{EVENT_TAG_CSV} {MESSAGE}"))

    def load_event_steps(self):
        """Загрузка этапов ивентов."""

        for row in DictReader(f=open(EVENT_STEPS_CSV, encoding=UTF)):
            start_time = datetime.datetime.strptime(
                row.pop("start_time"), "%H:%M"
            ).time()
            event = Event.objects.get(pk=row.get("event_id"))
            EventStep.objects.update_or_create(
                start_time=start_time,
                event=event,
                **row,
            )
        self.stdout.write(self.style.SUCCESS(f"{EVENT_STEPS_CSV} {MESSAGE}"))

    def load_event_steps_speakers(self):
        """Загрузка спикеров этапов ивентов рандомная загрузка."""

        speakers = list(Speaker.objects.all())
        speakers_number = len(speakers)
        event_steps = EventStep.objects.all()

        for step in event_steps:
            step_speakers_number = randint(1, speakers_number)
            for i in range(step_speakers_number):
                step.speakers.add(speakers[i])
                step.save()
        self.stdout.write(
            self.style.SUCCESS(f"{EVENT_STEPS_SPEAKERS_MESSAGE} {MESSAGE}")
        )

    def load_registrations(self):
        """Загрузка регистраций."""

        for row in DictReader(f=open(REGISTRATION_CSV, encoding=UTF)):
            event = Event.objects.get(pk=row.pop("event_id"))
            user = User.objects.get(pk=row.pop("user_id"))
            date_create = datetime.datetime.strptime(
                row.pop("date_create"), "%Y-%m-%d"
            )
            Registration.objects.update_or_create(
                event=event,
                user=user,
                date_create=date_create,
                **row,
            )
        self.stdout.write(self.style.SUCCESS(f"{REGISTRATION_CSV} {MESSAGE}"))

    def load_favorites(self):
        """Загрузка изьранных событий."""

        for row in DictReader(f=open(EVENT_FAVORITE_CSV, encoding=UTF)):
            user = User.objects.get(pk=row.get("user_id"))
            event = Event.objects.get(pk=row.get("event_id"))
            event.favorited_by.add(user)
            event.save()
            user.save()

        self.stdout.write(
            self.style.SUCCESS(f"{EVENT_FAVORITE_CSV} {MESSAGE}")
        )

    def handle(self, *args, **options):
        """Исполнение административной команды."""

        try:
            if User.objects.count() >= 0:
                self.load_tags()
                self.load_city()
                self.load_event_type()
                self.load_speaker()
                self.load_users()
                self.load_users_tags()
                self.load_users_cities()
                self.load_users_notifications()
                self.load_event()
                self.load_event_tags()
                self.load_event_steps()
                self.load_event_steps_speakers()
                self.load_registrations()
                self.load_favorites()
            else:
                self.stdout.write(
                    self.style.ERROR(
                        "До загрузки тестовых данных необходимо создать "
                        "пользователя - администратора проекта."
                    )
                )
        except IntegrityError as err:
            self.stdout.write(self.style.ERROR(f"ERROR - {err}"))
            exit()
