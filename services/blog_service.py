from __future__ import annotations

from typing import Any

from requests import Response

from utils.request_util import ApiClient


class BlogService:
    def __init__(self, client: ApiClient):
        self.client = client
        self.settings = client.settings

    def get_list(self, token: str | None = None) -> Response:
        headers = self.client.auth_headers(token) if token else None
        return self.client.get(self.settings.endpoint("blog", "list"), headers=headers)

    def get_detail(self, blog_id: int | str, token: str | None = None) -> Response:
        headers = self.client.auth_headers(token) if token else None
        return self.client.get(
            self.settings.endpoint("blog", "detail"),
            params={"id": blog_id},
            headers=headers,
        )

    def add_blog(self, title: str, content: str, token: str, **extra: Any) -> Response:
        payload = {"title": title, "content": content, **extra}
        return self.client.post(
            self.settings.endpoint("blog", "add"),
            json=payload,
            headers=self.client.auth_headers(token),
        )
