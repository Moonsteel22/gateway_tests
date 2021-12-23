import time

import pytest
from tests.classes.client_test import Client


@pytest.fixture(scope="session")
def get_client() -> Client:
    return Client(
        gateway_url="http://localhost:44777/api",
        user={
            "email": str(time.time())[:10] + "@mail.ru",
            "password": "123123123",
        },
    )
