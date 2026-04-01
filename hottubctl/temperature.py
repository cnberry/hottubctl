from __future__ import annotations

from .config import preferred_unit
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


async def list_spas() -> list[dict]:
    client = await login_client()
    try:
        account = await client.get_account()
        spas = await account.get_spas()
        return [
            {"id": spa.id, "name": spa.name, "brand": spa.brand, "model": spa.model}
            for spa in spas
        ]
    finally:
        await client._session.close()


async def get_temperature_status() -> dict:
    client = await login_client()
    try:
        spa = await select_spa(client)
        status = await spa.get_status()
        unit = preferred_unit()
        water_temp_c = None
        if getattr(status, "water", None) is not None:
            water_temp_c = getattr(status.water, "temperature", None)
        set_temp_c = getattr(status, "set_temperature", None)
        return {
            "spa_id": spa.id,
            "spa_name": spa.name,
            "display_temperature_format": getattr(status, "display_temperature_format", None),
            "heat_mode": getattr(getattr(status, "heat_mode", None), "name", getattr(status, "heat_mode", None)),
            "water_temp_c": water_temp_c,
            "set_temp_c": set_temp_c,
            "water_temp_display": format_temp(water_temp_c, unit),
            "set_temp_display": format_temp(set_temp_c, unit),
            "preferred_unit": unit,
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
