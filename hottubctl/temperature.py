from __future__ import annotations

from .config import preferred_unit
from .render import format_age, format_timestamp
from .smarttub_api import login_client, select_spa


def c_to_f(temp_c: float) -> float:
    return (temp_c * 9.0 / 5.0) + 32.0


def f_to_c(temp_f: float) -> float:
    return (temp_f - 32.0) * 5.0 / 9.0


def format_temp(temp_c: float | None, unit: str) -> str:
    if temp_c is None:
        return "unknown"
    unit = unit.upper()
    if unit == "F":
        return f"{c_to_f(temp_c):.1f}°F"
    return f"{temp_c:.1f}°C"


def _note_for_freshness(online: bool, telemetry_last_updated, water_last_updated) -> str:
    if not online:
        if telemetry_last_updated or water_last_updated:
            return "spa is offline; temperatures may be stale last-known values"
        return "spa is offline; no fresh telemetry available"
    if telemetry_last_updated is None and water_last_updated is None:
        return "spa is online, but SmartTub did not include telemetry timestamps"
    return "spa is online"


async def list_spas() -> list[dict]:
    client = await login_client()
    try:
        account = await client.get_account()
        spas = await account.get_spas()
        return [
            {"id": spa.id, "name": spa.name, "brand": spa.brand, "model": spa.model} for spa in spas
        ]
    finally:
        await client._session.close()


async def get_temperature_status() -> dict:
    client = await login_client()
    try:
        spa = await select_spa(client)
        status = await spa.get_status_full()
        unit = preferred_unit()
        water_temp_c = None
        if getattr(status, "water", None) is not None:
            water_temp_c = getattr(status.water, "temperature", None)
        set_temp_c = getattr(status, "set_temperature", None)
        online = bool(getattr(status, "online", False))
        telemetry_last_updated = getattr(status, "last_updated", None)
        water_last_updated = None
        connectivity_checked_at = None
        properties = getattr(status, "properties", {}) or {}
        water_props = properties.get("water") or {}
        fields_last_updated = getattr(status, "fields_last_updated", {}) or {}
        water_last_updated = water_props.get("temperatureLastUpdated") or water_props.get(
            "lastUpdated"
        )
        connectivity_checked_at = fields_last_updated.get("online")
        return {
            "spa_id": spa.id,
            "spa_name": spa.name,
            "display_temperature_format": getattr(status, "display_temperature_format", None),
            "heat_mode": getattr(
                getattr(status, "heat_mode", None), "name", getattr(status, "heat_mode", None)
            ),
            "online": online,
            "water_temp_c": water_temp_c,
            "set_temp_c": set_temp_c,
            "water_temp_display": format_temp(water_temp_c, unit),
            "set_temp_display": format_temp(set_temp_c, unit),
            "preferred_unit": unit,
            "telemetry_last_updated": telemetry_last_updated,
            "telemetry_last_updated_display": format_timestamp(telemetry_last_updated),
            "telemetry_age_display": format_age(telemetry_last_updated),
            "water_last_updated": water_last_updated,
            "water_last_updated_display": format_timestamp(water_last_updated),
            "water_age_display": format_age(water_last_updated),
            "connectivity_checked_at": connectivity_checked_at,
            "connectivity_checked_at_display": format_timestamp(connectivity_checked_at),
            "connectivity_age_display": format_age(connectivity_checked_at),
            "data_freshness_note": _note_for_freshness(
                online, telemetry_last_updated, water_last_updated
            ),
        }
    finally:
        await client._session.close()


async def set_temperature(value: float, unit: str | None = None) -> dict:
    client = await login_client()
    try:
        spa = await select_spa(client)
        use_unit = (unit or preferred_unit()).upper()
        target_c = value if use_unit == "C" else f_to_c(value)
        await spa.set_temperature(target_c)
        status = await spa.get_status()
        return {
            "spa_id": spa.id,
            "spa_name": spa.name,
            "requested_input": value,
            "requested_unit": use_unit,
            "set_temp_c": getattr(status, "set_temperature", None),
            "set_temp_display": format_temp(getattr(status, "set_temperature", None), use_unit),
        }
    finally:
        await client._session.close()
