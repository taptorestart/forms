import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tests.apis.factories import UserFactory


@pytest.fixture
def client_anonymous():
    client: APIClient = APIClient()
    return client


@pytest.fixture
def client_staff():
    user_staff: User = UserFactory(username="staff", is_staff=True)
    client: APIClient = APIClient()
    client.force_authenticate(user=user_staff)
    return client
