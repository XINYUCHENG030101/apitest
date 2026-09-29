from __future__ import annotations

from requests import Response

from utils.request_util import ApiClient


class UserService:
    def __init__(self, client: ApiClient):
        self.client = client
        self.settings = client.settings

    def login(self, username: str, password: str) -> Response:
        return self.client.post(
            self.settings.endpoint("user", "login"),
            data={"username": username, "password": password},
        )

    def get_user_info(self, token: str) -> Response:
        return self.client.get(
            self.settings.endpoint("user", "info"),
            headers=self.client.auth_headers(token),
        )

    def get_author_info(self, author_id: int | str, token: str) -> Response:
        return self.client.get(
            self.settings.endpoint("user", "author"),
            params={"id": author_id},
            headers=self.client.auth_headers(token),
        )
