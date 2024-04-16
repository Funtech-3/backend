from http import HTTPStatus

import pytest
from events.models import Event


@pytest.mark.django_db(transaction=True)
class TestEventAPI:
    """Тесты эндпоинтов для списка событий и конкретного события."""

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

    def test_event_list_auth(self, user_client, url_event_list):
        response = user_client.get(url_event_list)
        assert response.status_code == HTTPStatus.OK, (
            f"Эндпоинт {url_event_list} должен быть доступен"
            f"авторизованным пользователям."
        )

    def test_events_get_paginated(self, client, url_event_list, event_list):
        limit = 3
        offset = 3
        url = f"{url_event_list}?limit={limit}&offset={offset}"
        response = client.get(url)
        assert response.status_code == 200, (
            "Убедитесь, что GET-запрос с параметрами `limit` и `offset`, "
            "отправленный неавторизованным пользователем к "
            f"`{url_event_list}`, возвращает ответ со статусом 200."
        )
        test_data = response.json()
        assert isinstance(test_data, dict), (
            "GET-запрос с параметрами `limit` и `offset`, "
            "отправленный неавторизованным пользователем к "
            f"`{url_event_list}`, возвращает {type(test_data)}."
        )
        assert "results" in test_data, (
            "GET-запрос с параметрами `limit` и `offset`, "
            "отправленный неавторизованным пользователем к эндпоинту "
            f"`{url_event_list}`, содержит поле `results` с данными "
            "событий. Проверьте настройку пагинации для этого эндпоинта."
        )
        results = test_data["results"]
        assert len(results) == Event.objects.count() - offset, (
            "Убедитесь, что GET-запрос с параметрами `limit` и `offset`, "
            "отправленный неавторизованным пользователем к эндпоинту "
            f"`{url_event_list}`, возвращает корректное количество событий."
        )

    def test_event_detail_not_auth(self, client, url_event_detail, event):
        response = client.get(url_event_detail)
        assert response.status_code == HTTPStatus.OK, (
            f"Эндпоинт {url_event_detail} должен быть доступен"
            f"неавторизованным пользователям."
        )
        data = response.json()
        assert isinstance(data, dict), (
            f"Проверьте, что GET-запрос к {url_event_detail}"
            "возвращает словарь."
        )

    def test_event_detail_auth(self, user_client, url_event_detail):
        response = user_client.get(url_event_detail)
        assert response.status_code == HTTPStatus.OK, (
            f"Эндпоинт {url_event_detail} должен быть доступен"
            f"неавторизованным пользователям."
        )

    def test_favorite_post_not_auth(self, client, event, url_event_favorite):
        response = client.post(url_event_favorite)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "У анонимных пользователей не должно быть возможности "
            "добавить событие в избранное."
        )

    def test_favorite_post_auth(self, user_client, url_event_favorite, event):
        response = user_client.post(url_event_favorite)
        assert response.status_code == HTTPStatus.CREATED
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "is_in_favorites" in response_data
        assert response_data["is_in_favorites"]

    def test_favorite_delete_auth(
        self, user_client, url_event_favorite, user, event
    ):
        event.favorited_by.add(user)
        response = user_client.delete(url_event_favorite)
        assert response.status_code == HTTPStatus.NO_CONTENT
