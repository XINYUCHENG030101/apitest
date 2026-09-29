from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from requests import Response


@dataclass(frozen=True)
class LoginUserScenarioResult:
    token: str
    login_response: Response
    user_info_response: Response


@dataclass(frozen=True)
class AuthorFromFirstBlogScenarioResult:
    blog: dict[str, Any]
    list_response: Response
    author_response: Response


@dataclass(frozen=True)
class CreateBlogScenarioResult:
    blog_id: int | str
    created_blog: dict[str, Any]
    add_response: Response
    list_response: Response
    detail_response: Response
