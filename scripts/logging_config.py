#!/usr/bin/env python3
"""
SWEBOK v4 Harness V2 — Logging Configuration
============================================

stdlib logging configured for the harness:
- JSON formatter for production
- Human-readable for dev
- Levels: DEBUG, INFO, WARNING, ERROR
- Per-module loggers
- Configurable via SWEBOK_LOG_LEVEL env var

Usage:
    from logging_config import get_logger
    log = get_logger(__name__)
    log.info("indexed %d chunks", n)
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone

_DEFAULT_LEVEL = os.environ.get("SWEBOK_LOG_LEVEL", "WARNING").upper()
_DEFAULT_FORMAT = os.environ.get("SWEBOK_LOG_FORMAT", "text")  # "text" or "json"


class JSONFormatter(logging.Formatter):
    """Emit structured JSON log lines."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        # Include any extra fields
        for k, v in record.__dict__.items():
            if k.startswith("_") or k in ("msg", "args", "levelname", "levelno", "pathname", "filename", "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName", "created", "msecs", "relativeCreated", "thread", "threadName", "processName", "process", "name", "taskName"):
                continue
            payload[k] = v
        return json.dumps(payload, ensure_ascii=False)


_TEXT_FORMAT = "%(asctime)s %(levelname)-7s [%(name)s] %(message)s"


def configure(level: str = None, fmt: str = None) -> None:
    """Configure the root logger once."""
    level = (level or _DEFAULT_LEVEL).upper()
    fmt = fmt or _DEFAULT_FORMAT
    root = logging.getLogger()
    if root.handlers:
        return  # already configured
    root.setLevel(getattr(logging, level, logging.WARNING))
    handler = logging.StreamHandler(sys.stderr)
    if fmt == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter(_TEXT_FORMAT))
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a module-level logger. Auto-configures the root on first call."""
    configure()
    return logging.getLogger(name)
