from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestEventAPI:
    """Тесты эндпоинтов для списка событий и конкретного события."""

    def check_event_response_data(self, response_data, expected_fields):
        for field in expected_fields:
            assert field in response_data, ()

    def test_events_not_found(self, client, url_event_list):
        response = client.get(url_event_list)
        assert (
            response.status_code != HTTPStatus.NOT_FOUND
        ), f"Эндпоинт {url_event_list} не найден."

    def test_event_list_not_auth(self, client, url_event_list):
        response = client.get(url_event_list)
        assert response.status_code == HTTPStatus.OK, (
            f"Эндпоинт {url_event_list} должен быть доступен"
            f"неавторизованным пользователям."
        )

    def test_event_detail_not_auth(self, client, url_event_detail):
        response = client.get(url_event_detail)
        assert response.status_code == HTTPStatus.OK, (
            f"Эндпоинт {url_event_detail} должен быть доступен"
            f"неавторизованным пользователям."
        )
