from http import HTTPStatus

import pytest
from tickets.models import Registration


@pytest.mark.django_db(transaction=True)
class TestTicketAPI:

    def test_registration_not_auth(
        self, client, url_event_registration, event
    ):
        response = client.post(url_event_registration)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Запрос неавторизованного пользователя зарегистрироваться "
            f"на событие должен возвращать {HTTPStatus.UNAUTHORIZED}"
        )

        assert Registration.objects.count() == 0, (
            "У анонимных пользователей не должно быть возможности "
            "зарегистрироваться на событие."
        )

    def test_registration_auth(
        self, user_client, user, event, url_event_registration
    ):
        response = user_client.post(url_event_registration)
        assert response.status_code == HTTPStatus.CREATED
        assert Registration.objects.count() == 1, (
            "Проверьте, что у авторизованного пользователя есть "
            "возможность зарегистрироваться на событие."
        )
        db_registration = Registration.objects.all()[0]
        assert db_registration.user == user
        assert db_registration.event == event

    def test_ticket_get_not_auth(self, client, registration, url_user_ticket):
        response = client.get(url_user_ticket)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Запрос неавторизованного пользователя на чтение билета "
            f"должен возвращать {HTTPStatus.UNAUTHORIZED}"
        )

    def test_ticket_get_owner(
        self, user_client, registration, url_user_ticket
    ):
        response = user_client.get(url_user_ticket)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert isinstance(response_data, dict)
        expected_fields = {
            "ticket_id": registration.ticket_id,
            "city": registration.event.city.name,
            "code": registration.code,
            "name": registration.event.title,
            "date_event": registration.event.date.isoformat(),
        }
        assert response_data == expected_fields

    def test_ticket_get_not_owner(
        self, another_user_client, registration, url_user_ticket
    ):
        response = another_user_client.get(url_user_ticket)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            "Возможность посмотреть информацию о билете "
            "должна быть только у его владельца."
        )

    def test_ticket_delete_not_auth(
        self, client, registration, url_user_ticket
    ):
        response = client.delete(url_user_ticket)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert Registration.objects.filter(pk=registration.pk).exists(), (
            "У неавторизованного пользователя не должно быть возможности "
            "удалить билет."
        )

    def test_ticket_delete_not_owner(
        self, another_user_client, registration, url_user_ticket
    ):
        response = another_user_client.delete(url_user_ticket)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert Registration.objects.filter(pk=registration.pk).exists(), (
            "У авторизованного пользователя не должно быть возможности "
            "удалить чужой билет."
        )

    def test_ticket_delete_owner(
        self, user_client, registration, url_user_ticket
    ):
        response = user_client.delete(url_user_ticket)
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not Registration.objects.filter(pk=registration.pk).exists(), (
            "У авторизованного пользователя должна быть возможность "
            "удалить свой билет."
        )
