import json
from uuid import uuid4

from pytest import fixture
from tests.classes.client_test import Client


class BaseTestAPI:
    client: Client

    @fixture(scope="session", autouse=True)
    def setup(self, get_client):
        type(self).client = get_client


class TestAPI(BaseTestAPI):
    def test_get_user(self):
        response = self.client.request.get(
            url=self.client.gateway_url + "/users",
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
            },
        )

        assert response.status_code == 200

    def test_upload_function(self):
        files = {}

        files = {
            "meta": (
                None,
                json.dumps(
                    {
                        "lang_name": "python",
                        "lang_version": "3.9",
                        "entrypoint": "main.handler",
                    },
                ),
                "application/json",
            ),
            "main.py": (
                "main.py",
                open("tests/files/main.py"),
                "application/octet-stream",
            ),
            "requirements.txt": (
                "requirements.txt",
                open("tests/files/requirements.txt"),
                "application/octet-stream",
            ),
        }

        response = self.client.request.post(
            url=self.client.gateway_url + f"/functions/{str(uuid4())}",
            files=files,
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
            },
        )
        assert response.status_code == 201

    def test_run_function(self):
        function = str(uuid4()).replace("-", "")
        files = {
            "meta": (
                None,
                json.dumps(
                    {
                        "lang_name": "python",
                        "lang_version": "3.9",
                        "entrypoint": "main.handler",
                    },
                ),
                "application/json",
            ),
            "main.py": (
                "main",
                open("tests/files/main.py"),
                "application/octet-stream",
            ),
            "requirements.txt": (
                "requirements.txt",
                open("tests/files/requirements.txt"),
                "application/octet-stream",
            ),
        }
        response = self.client.request.post(
            url=self.client.gateway_url + f"/functions/{function}",
            files=files,
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
            },
        )
        assert response.status_code == 201

        host_config = {
            "HostConfig": {
                "CpuQuota": "1",
                "CpuPeriod": "1000",
                "CpuCount": "500",
                "Memory": "512",
            },
            "timeout": "10",
        }

        response = self.client.request.post(
            url=self.client.gateway_url + f"/functions/run/{function}",
            data=json.dumps(host_config),
            headers={
                "Authorization": f"Bearer {self.client.access_token}",
                "Content-Type": "application/json",
            },
        )
        response_body = response.json()
        assert response.status_code == 200
        assert "StatusCode" in response_body
        assert "Headers" in response_body
        assert "Body" in response_body
