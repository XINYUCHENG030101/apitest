from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from utils.config_util import PROJECT_ROOT


def _resolve_path(filename: str | Path, base_dir: str | Path = "data") -> Path:
    path = Path(filename)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == str(base_dir):
        return PROJECT_ROOT / path
    return PROJECT_ROOT / base_dir / path


def load_yaml(filename: str | Path, base_dir: str | Path = "data") -> Any:
    path = _resolve_path(filename, base_dir)
    if not path.exists():
        raise FileNotFoundError(f"YAML 文件不存在: {path}")
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_cases(filename: str | Path, key: str | None = None) -> list[dict[str, Any]]:
    data = load_yaml(filename)
    if key is not None:
        if not isinstance(data, dict) or key not in data:
            raise KeyError(f"YAML 中不存在数据集: {key}")
        data = data[key]
    if not isinstance(data, list):
        raise TypeError(f"参数化数据必须是列表: {filename}")
    return data


def case_ids(cases: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("id", index)) for index, item in enumerate(cases)]


def read_yaml(filename: str | Path, key: str | None = None) -> Any:
    data = load_yaml(filename)
    return data[key] if key is not None else data


def write_yaml(filename: str | Path, data: Any) -> None:
    path = _resolve_path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_yaml(path) if path.exists() else {}
    if isinstance(existing, dict) and isinstance(data, dict):
        existing.update(data)
        data = existing
    with path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)


def clear_yaml(filename: str | Path) -> None:
    path = _resolve_path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
