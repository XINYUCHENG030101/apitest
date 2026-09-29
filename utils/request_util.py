from __future__ import annotations

import json
import time
from typing import Any
from urllib.parse import urljoin

import allure
import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.config_util import Settings, get_settings
from utils.log_util import get_logger

_SENSITIVE_KEYS = {"authorization", "password", "token", "access_token", "user_token_header"}


def _mask(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "***" if key.lower() in _SENSITIVE_KEYS else _mask(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_mask(item) for item in value]
    return value


def _as_text(value: Any) -> str:
    try:
        return json.dumps(_mask(value), ensure_ascii=False, indent=2, default=str)
    except (TypeError, ValueError):
        return str(value)


class ApiClient:
    def __init__(self, settings: Settings | None = None, session: Session | None = None):
        self.settings = settings or get_settings()
        self.session = session or requests.Session()
        self.log = get_logger("apitest.http", self.settings)
        retry = Retry(
            total=2,
            connect=2,
            read=0,
            status=0,
            backoff_factor=0.2,
            allowed_methods=frozenset({"GET", "HEAD", "OPTIONS"}),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        url = path if path.startswith(("http://", "https://")) else urljoin(
            f"{self.settings.base_url}/", path.lstrip("/")
        )
        kwargs.setdefault("timeout", self.settings.timeout)
        kwargs.setdefault("verify", self.settings.verify_ssl)
        request_context = {
            "method": method.upper(),
            "url": url,
            "params": kwargs.get("params"),
            "headers": kwargs.get("headers"),
            "json": kwargs.get("json"),
            "data": kwargs.get("data"),
        }
        self.log.info("HTTP request\n%s", _as_text(request_context))
        started = time.perf_counter()

        try:
            response = self.session.request(method=method, url=url, **kwargs)
        except requests.RequestException as exc:
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            error_context = {**request_context, "elapsed_ms": elapsed_ms, "error": repr(exc)}
            self.log.exception("HTTP request failed\n%s", _as_text(error_context))
            self._attach("request-error", error_context)
            raise

        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        response_context = {
            "status_code": response.status_code,
            "elapsed_ms": elapsed_ms,
            "headers": dict(response.headers),
            "body": self._response_body(response),
        }
        self.log.info("HTTP response\n%s", _as_text(response_context))
        self._attach("request", request_context)
        self._attach("response", response_context)
        response.apitest_context = {"request": request_context, "response": response_context}
        return response

    def get(self, path: str, **kwargs: Any) -> Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        return self.request("DELETE", path, **kwargs)

    def auth_headers(self, token: str) -> dict[str, str]:
        return {self.settings.token_header: token}

    def close(self) -> None:
        self.session.close()

    @staticmethod
    def _response_body(response: Response) -> Any:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return response.text[:5000]

    @staticmethod
    def _attach(name: str, value: Any) -> None:
        try:
            allure.attach(
                _as_text(value),
                name=name,
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            pass


class request(ApiClient):
    pass


host = f"{get_settings().base_url}/"
