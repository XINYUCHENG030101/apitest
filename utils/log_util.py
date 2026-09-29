from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.config_util import PROJECT_ROOT, Settings, get_settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(name: str = "apitest", settings: Settings | None = None) -> logging.Logger:
    config = settings or get_settings()
    logger = logging.getLogger(name)
    if getattr(logger, "_apitest_configured", False):
        return logger

    level_name = str(config.get("logging.level", "INFO")).upper()
    logger.setLevel(getattr(logging, level_name, logging.INFO))
    logger.propagate = False
    formatter = logging.Formatter(_LOG_FORMAT)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    log_dir = Path(config.get("logging.directory", "logs"))
    if not log_dir.is_absolute():
        log_dir = PROJECT_ROOT / log_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_dir / "apitest.log",
        maxBytes=int(config.get("logging.max_bytes", 5 * 1024 * 1024)),
        backupCount=int(config.get("logging.backup_count", 5)),
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger._apitest_configured = True
    return logger


class logger:
    @classmethod
    def getlog(cls) -> logging.Logger:
        return get_logger()
