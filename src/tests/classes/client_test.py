import requests


class Client:
    def __init__(self, gateway_url, user) -> None:
        self.gateway_url = gateway_url
        self.request = requests.sessions.Session()
        self.user = user
        self._register_user()
        self._get_token()

    def _register_user(self) -> None:
        self.request.post(url=self.gateway_url + "/users", json=self.user)

    def _get_token(self) -> None:
        response = self.request.post(
            url=self.gateway_url + "/jwt/create",
            json=self.user,
        )
        tokens = response.json()
        self.access_token = tokens["access"]
        self.refresh_token = tokens["refresh"]
