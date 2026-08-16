import json

import pytest

from hottubctl.config import (
    ConfigError,
    preferred_spa_selector,
    preferred_unit,
    smarttub_credentials,
)


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


def test_password_can_come_from_environment(monkeypatch, tmp_path):
    write_config(monkeypatch, tmp_path, {"username": "user@example.com"})
    monkeypatch.setenv("HOTTUBCTL_PASSWORD", "environment-only")
    assert smarttub_credentials() == ("user@example.com", "environment-only")


def test_rejects_invalid_temperature_unit(monkeypatch, tmp_path):
    write_config(monkeypatch, tmp_path, {"temperature_unit": "kelvin"})
    with pytest.raises(ConfigError, match="must be F or C"):
        preferred_unit()
