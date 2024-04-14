import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        yandex_id=11111
    )


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create(
        yandex_id=22222
    )


@pytest.fixture
def token(user):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


@pytest.fixture
def user_client(user, token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
    return client
