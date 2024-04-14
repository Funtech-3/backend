from django.urls import reverse
import pytest


@pytest.fixture
def url_event_list():
    return reverse('event-list')


@pytest.fixture
def url_event_detail(event):
    return reverse('event-detail', args=(event.slug,))
