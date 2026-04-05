from __future__ import annotations

from datetime import datetime, timezone


def _coerce_datetime(value: datetime | str | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    return None


def format_timestamp(value: datetime | str | None) -> str:
    value = _coerce_datetime(value)
    if value is None:
        return "unknown"
    local = value.astimezone()
    return local.strftime("%Y-%m-%d %H:%M:%S %Z")


def format_age(value: datetime | str | None, now: datetime | None = None) -> str:
    value = _coerce_datetime(value)
    if value is None:
        return "unknown"
    now = now or datetime.now(timezone.utc)
    delta = now - value.astimezone(timezone.utc)
    seconds = max(int(delta.total_seconds()), 0)
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m"
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h {minutes}m"
    days, hours = divmod(hours, 24)
    if days < 7:
        return f"{days}d {hours}h"
    weeks, days = divmod(days, 7)
    return f"{weeks}w {days}d"


def render_temperature_status(status: dict) -> str:
    lines = [
        "Hot tub status",
        "--------------",
        f"- Spa: {status['spa_name']} ({status['spa_id']})",
        f"- Connectivity: {'ONLINE' if status['online'] else 'OFFLINE'}",
    ]

    if status.get("connectivity_checked_at_display"):
        lines.append(
            f"- Connectivity checked: {status['connectivity_checked_at_display']} ({status['connectivity_age_display']} ago)"
        )

    lines.extend(
        [
            f"- Water: {status['water_temp_display']}",
            f"- Set: {status['set_temp_display']}",
        ]
    )

    if status.get("heat_mode"):
        lines.append(f"- Heat mode: {status['heat_mode']}")

    if status.get("telemetry_last_updated_display"):
        lines.append(
            f"- Telemetry updated: {status['telemetry_last_updated_display']} ({status['telemetry_age_display']} ago)"
        )

    if status.get("water_last_updated_display"):
        lines.append(
            f"- Water reading updated: {status['water_last_updated_display']} ({status['water_age_display']} ago)"
        )

    if status.get("data_freshness_note"):
        lines.append(f"- Note: {status['data_freshness_note']}")

    return "\n".join(lines)
