import pytest
from rest_framework.test import APIClient


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(yandex_id=11111)


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create(yandex_id=22222)


@pytest.fixture
def token(user):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@pytest.fixture
def user_client(user, token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
    return client


@pytest.fixture
def another_user_client(another_user):
    another_user_client = APIClient()
    another_user_client.force_login(another_user)
    return another_user_client
