import pytest
from django.urls import reverse


@pytest.fixture
def url_event_list():
    return reverse("event-list")


@pytest.fixture
def url_event_detail(event):
    return reverse("event-detail", args=(event.slug,))


@pytest.fixture
def url_event_favorite(event):
    return reverse("event-favorite", args=(event.slug,))


@pytest.fixture
def url_event_registration(event):
    return reverse("event-registration", args=(event.slug,))


@pytest.fixture
def url_user_ticket(registration):
    return reverse("ticket-detail", args=(registration.pk,))
