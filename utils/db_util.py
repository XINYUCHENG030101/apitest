from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

from utils.config_util import Settings, get_settings


class DatabaseClient:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.config = self.settings.get("database", {})

    @property
    def enabled(self) -> bool:
        return bool(self.config.get("enabled", False))

    @contextmanager
    def connection(self) -> Iterator[Any]:
        if not self.enabled:
            raise RuntimeError("数据库校验未启用，请在 config/settings.yml 中设置 database.enabled")
        if self.config.get("driver") != "mysql":
            raise ValueError(f"暂不支持数据库驱动: {self.config.get('driver')}")
        try:
            import pymysql
        except ImportError as exc:
            raise RuntimeError("启用 MySQL 校验前请安装 pymysql") from exc

        connection = pymysql.connect(
            host=self.config["host"],
            port=int(self.config.get("port", 3306)),
            user=self.config["username"],
            password=self.config["password"],
            database=self.config["database"],
            charset=self.config.get("charset", "utf8mb4"),
            cursorclass=pymysql.cursors.DictCursor,
        )
        try:
            yield connection
        finally:
            connection.close()

    def fetch_one(self, sql: str, params: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
        with self.connection() as connection, connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def fetch_all(self, sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        with self.connection() as connection, connection.cursor() as cursor:
            cursor.execute(sql, params)
            return list(cursor.fetchall())
