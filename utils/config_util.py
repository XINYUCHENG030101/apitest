from __future__ import annotations

import copy
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SETTINGS_PATH = PROJECT_ROOT / "config" / "settings.yml"


class ConfigError(RuntimeError):
    pass


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


@lru_cache(maxsize=4)
def load_settings(path: str | Path = DEFAULT_SETTINGS_PATH) -> dict[str, Any]:
    settings_path = Path(path)
    if not settings_path.is_absolute():
        settings_path = PROJECT_ROOT / settings_path
    if not settings_path.exists():
        raise ConfigError(f"配置文件不存在: {settings_path}")

    with settings_path.open("r", encoding="utf-8") as file:
        settings = yaml.safe_load(file) or {}
    if not isinstance(settings, dict):
        raise ConfigError("settings.yml 顶层必须是对象")
    return settings


class Settings:
    def __init__(self, env: str | None = None, path: str | Path = DEFAULT_SETTINGS_PATH):
        self._raw = copy.deepcopy(load_settings(path))
        self.env = env or os.getenv("APITEST_ENV") or self._raw.get("active_env", "test")
        environments = self._raw.get("environments", {})
        if self.env not in environments:
            raise ConfigError(f"未配置环境 {self.env!r}，可选值: {', '.join(environments)}")
        self._data = _deep_merge(self._raw, environments[self.env])

    def get(self, path: str, default: Any = None, *, required: bool = False) -> Any:
        value: Any = self._data
        for key in path.split("."):
            if not isinstance(value, dict) or key not in value:
                if required:
                    raise ConfigError(f"缺少配置项: {path}")
                return default
            value = value[key]
        return value

    @property
    def base_url(self) -> str:
        return str(self.get("base_url", required=True)).rstrip("/")

    @property
    def timeout(self) -> float:
        return float(self.get("timeout", 10))

    @property
    def verify_ssl(self) -> bool:
        return bool(self.get("verify_ssl", True))

    @property
    def token_header(self) -> str:
        return str(self.get("auth.token_header", "Authorization"))

    def endpoint(self, domain: str, name: str) -> str:
        return str(self.get(f"endpoints.{domain}.{name}", required=True))

    def account(self, name: str = "default") -> dict[str, str]:
        account = self.get(f"accounts.{name}", required=True)
        return {str(key): str(value) for key, value in account.items()}

    def resolve_path(self, path: str | Path) -> Path:
        candidate = Path(path)
        return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate


def get_settings(env: str | None = None) -> Settings:
    return Settings(env=env)
