"""Small .env loader so the starter has no extra runtime dependency."""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


def get_bool(key: str, default: bool = False) -> bool:
    raw = os.getenv(key)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def get_list(key: str, default: list[str] | None = None) -> list[str]:
    raw = os.getenv(key)
    if not raw:
        return list(default or [])
    return [item.strip() for item in raw.split(",") if item.strip()]
