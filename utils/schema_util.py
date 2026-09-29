from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator

RESPONSE_BASE = {
    "type": "object",
    "required": ["code", "errMsg"],
    "properties": {
        "code": {"type": "string"},
        "errMsg": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}

LOGIN_RESPONSE_SCHEMA = {
    **RESPONSE_BASE,
    "properties": {
        **RESPONSE_BASE["properties"],
        "data": {"type": ["string", "null"]},
    },
}

BLOG_ITEM_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "content", "userId"],
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "userId": {"type": "number"},
        "deleteFlag": {"type": "integer"},
        "createTime": {"type": "string"},
        "updateTime": {"type": "string"},
        "loginUser": {"type": "boolean"},
    },
    "additionalProperties": True,
}

BLOG_LIST_RESPONSE_SCHEMA = {
    **RESPONSE_BASE,
    "properties": {
        **RESPONSE_BASE["properties"],
        "data": {"type": "array", "items": BLOG_ITEM_SCHEMA},
    },
}

BLOG_DETAIL_RESPONSE_SCHEMA = {
    **RESPONSE_BASE,
    "properties": {
        **RESPONSE_BASE["properties"],
        "data": {"anyOf": [BLOG_ITEM_SCHEMA, {"type": "null"}]},
    },
}

USER_INFO_RESPONSE_SCHEMA = {
    **RESPONSE_BASE,
    "properties": {
        **RESPONSE_BASE["properties"],
        "data": {"type": ["object", "null"]},
    },
}


def assert_schema(instance: Any, schema: dict[str, Any], name: str = "response") -> None:
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    if not errors:
        return
    messages = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        messages.append(f"{location}: {error.message}")
    raise AssertionError(f"{name} Schema 校验失败:\n" + "\n".join(messages))
