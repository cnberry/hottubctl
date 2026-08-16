import pytest

from hottubctl.temperature import _note_for_freshness, c_to_f, f_to_c, format_temp


def test_temperature_conversions_round_trip():
    assert c_to_f(38) == pytest.approx(100.4)
    assert f_to_c(100.4) == pytest.approx(38)
    assert format_temp(38, "F") == "100.4°F"
    assert format_temp(38, "C") == "38.0°C"


def test_offline_freshness_notes_are_explicit():
    assert "last-known" in _note_for_freshness(False, "timestamp", None)
    assert "no fresh telemetry" in _note_for_freshness(False, None, None)
    assert _note_for_freshness(True, "timestamp", None) == "spa is online"
