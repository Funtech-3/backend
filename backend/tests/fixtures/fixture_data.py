from datetime import date, time, timedelta
from tempfile import NamedTemporaryFile

import pytest

from events.models import Event, EventStep, Speaker
from tickets.models import Registration
from users.models import City, Tag

LEN_OBJ_IN_LIST = 5


@pytest.fixture
def cities_list(db):
    return City.objects.bulk_create(
        City(name=f"Город {index}") for index in range(LEN_OBJ_IN_LIST)
    )


@pytest.fixture
def city(db):
    return City.objects.create(name="Тестовый город")


@pytest.fixture
def tags_list(db):
    return Tag.objects.bulk_create(
        Tag(title=f"Тег {index}") for index in range(LEN_OBJ_IN_LIST)
    )


@pytest.fixture
def tag(db):
    return Tag.objects.create(title="Тестовый тег")


@pytest.fixture
def speaker(db):
    return Speaker.objects.create(
        first_name="Иван",
        last_name="Иванов",
        work_place="ACME",
        position="Работник",
    )


@pytest.fixture
def image():
    return NamedTemporaryFile(suffix=".jpg").name


@pytest.fixture
def event(db, city, image, tag):
    event = Event.objects.create(
        title="Тестовое событие",
        description="Тестовое",
        slug="test-event",
        city=city,
        address="Зимний дворец",
        date=date.today() + timedelta(days=7),
        image=image,
    )
    event.tags.add(tag)
    return event


@pytest.fixture
def event_list(db, city, image):
    return Event.objects.bulk_create(
        Event(
            title=f"Тестовое событие {index}",
            description="Тестовое",
            slug=f"test-event-{index}",
            city=city,
            address="Зимний дворец",
            date=date.today() + timedelta(days=index),
            image=image,
        )
        for index in range(LEN_OBJ_IN_LIST)
    )


@pytest.fixture
def event_steps(db, events, speaker):
    steps = EventStep.objects.bulk_create(
        EventStep(
            title=f"Этап события {index}",
            start_time=time(hour=index),
            description=f"Событие {index}",
            event=event,
        )
        for index, event in enumerate(events)
    )
    for step in steps:
        step.speakers.add(speaker)
    return steps


@pytest.fixture
def registration(db, event, user):
    return Registration.objects.create(
        event=event, user=user, status=Registration.Status.CONFIRMED
    )
