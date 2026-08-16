from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

ENV_CONFIG_PATH = "HOTTUBCTL_CONFIG"
ENV_USERNAME = "HOTTUBCTL_USERNAME"
ENV_PASSWORD = "HOTTUBCTL_PASSWORD"
DEFAULT_CONFIG_BASENAME = "hottubctl.json"
SEARCH_DIRS = [
    Path.home() / ".config" / "hottubctl",
    Path.home() / ".hottubctl",
]
EXAMPLE_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "hottubctl.example.json"


class ConfigError(RuntimeError):
    pass


def config_path() -> Path:
    override = os.environ.get(ENV_CONFIG_PATH)
    if override:
        return Path(override).expanduser()
    for directory in SEARCH_DIRS:
        candidate = directory / DEFAULT_CONFIG_BASENAME
        if candidate.exists():
            return candidate
    return SEARCH_DIRS[0] / DEFAULT_CONFIG_BASENAME


def load_config() -> dict[str, Any]:
    path = config_path()
    if not path.exists():
        raise ConfigError(
            f"config not found at {path}. create it from {EXAMPLE_CONFIG_PATH} or set {ENV_CONFIG_PATH}"
        )
    with path.open() as f:
        return json.load(f)


def smarttub_credentials() -> tuple[str, str]:
    config = load_config()
    username = os.environ.get(ENV_USERNAME) or config.get("username")
    password = os.environ.get(ENV_PASSWORD) or config.get("password")
    if not username or not password:
        raise ConfigError(
            f"credentials require username and password in config or {ENV_USERNAME}/{ENV_PASSWORD}"
        )
    return username, password


def preferred_spa_selector() -> tuple[str | None, str | None]:
    config = load_config()
    return config.get("spa_name"), config.get("spa_id")


def preferred_unit() -> str:
    config = load_config()
    unit = str(config.get("temperature_unit", "F")).upper()
    if unit not in {"F", "C"}:
        raise ConfigError("temperature_unit must be F or C")
    return unit
