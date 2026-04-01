from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "hottubctl.json"
ENV_CONFIG_PATH = "HOTTUBCTL_CONFIG"


class ConfigError(RuntimeError):
    pass


def config_path() -> Path:
    override = os.environ.get(ENV_CONFIG_PATH)
    if override:
        return Path(override).expanduser()
    return DEFAULT_CONFIG_PATH


def load_config() -> dict[str, Any]:
    path = config_path()
    if not path.exists():
        raise ConfigError(
            "config/hottubctl.json not found. create it from config/hottubctl.example.json"
        )
    with path.open() as f:
        return json.load(f)


def smarttub_credentials() -> tuple[str, str]:
    config = load_config()
    username = config.get("username")
    password = config.get("password")
    if not username or not password:
        raise ConfigError("config requires username and password")
    return username, password


def preferred_spa_selector() -> tuple[str | None, str | None]:
    config = load_config()
    return config.get("spa_name"), config.get("spa_id")


def preferred_unit() -> str:
    config = load_config()
    return str(config.get("temperature_unit", "F")).upper()
