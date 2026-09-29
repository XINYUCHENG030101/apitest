from __future__ import annotations

from typing import Any

from requests import Response


class ApiAssert:
    @staticmethod
    def status_code(response: Response, expected: int = 200) -> None:
        assert response.status_code == expected, (
            f"HTTP 状态码不符，期望 {expected}，实际 {response.status_code}；"
            f"响应: {response.text[:1000]}"
        )

    @staticmethod
    def success(response: Response, code: str = "SUCCESS") -> dict[str, Any]:
        ApiAssert.status_code(response)
        body = ApiAssert.json_body(response)
        assert body.get("code") == code, f"业务码不符: {body}"
        return body

    @staticmethod
    def business_error(
        response: Response,
        message: str,
        code: str = "FAIL",
        status_code: int = 200,
    ) -> dict[str, Any]:
        ApiAssert.status_code(response, status_code)
        body = ApiAssert.json_body(response)
        assert body.get("code") == code, f"业务码不符: {body}"
        assert body.get("errMsg") == message, f"错误信息不符: {body}"
        return body

    @staticmethod
    def json_body(response: Response) -> dict[str, Any]:
        try:
            body = response.json()
        except ValueError as exc:
            raise AssertionError(f"响应不是合法 JSON: {response.text[:1000]}") from exc
        assert isinstance(body, dict), f"响应 JSON 顶层应为对象，实际为 {type(body).__name__}"
        return body

    @staticmethod
    def contains(container: Any, member: Any, message: str | None = None) -> None:
        assert member in container, message or f"{member!r} 不在 {container!r} 中"

    @staticmethod
    def not_empty(value: Any, message: str = "值不应为空") -> None:
        assert value not in (None, "", [], {}), message
