import json

import pytest

from hottubctl.config import (
    CONFIG_CANDIDATES,
    ConfigError,
    preferred_spa_selector,
    preferred_unit,
    smarttub_credentials,
)


def test_system_config_path_is_the_primary_default():
    assert CONFIG_CANDIDATES[0].as_posix() == "/usr/local/config/hottubctl/config.json"


def write_config(monkeypatch, tmp_path, payload):
    path = tmp_path / "hottubctl.json"
    path.write_text(json.dumps(payload))
    monkeypatch.setenv("HOTTUBCTL_CONFIG", str(path))
    return path


def test_loads_private_config_override(monkeypatch, tmp_path):
    write_config(
        monkeypatch,
        tmp_path,
        {
            "username": "user@example.com",
            "password": "example-only",
            "spa_name": "Example Spa",
            "temperature_unit": "f",
        },
    )
    assert smarttub_credentials() == ("user@example.com", "example-only")
    assert preferred_spa_selector() == ("Example Spa", None)
    assert preferred_unit() == "F"


def test_rejects_missing_password(monkeypatch, tmp_path):
    write_config(monkeypatch, tmp_path, {"username": "user@example.com"})
    with pytest.raises(ConfigError, match="username and password in config"):
        smarttub_credentials()


def test_rejects_invalid_temperature_unit(monkeypatch, tmp_path):
    write_config(monkeypatch, tmp_path, {"temperature_unit": "kelvin"})
    with pytest.raises(ConfigError, match="must be F or C"):
        preferred_unit()
