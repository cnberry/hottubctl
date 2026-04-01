from __future__ import annotations

import argparse
import asyncio
import json
import sys

from .config import ConfigError
from .smarttub_api import SpaSelectionError
from .temperature import get_temperature_status, list_spas, set_temperature


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hottubctl", description="Terminal-first Sundance SmartTub control")
    sub = parser.add_subparsers(dest="command", required=True)

    spas = sub.add_parser("spas", help="list SmartTub spas visible to the account")
    spas.add_argument("--json", action="store_true", help="emit raw JSON")

    temp = sub.add_parser("temp", help="get or set spa temperature")
    temp_sub = temp.add_subparsers(dest="temp_command", required=True)

    temp_get = temp_sub.add_parser("get", help="show current and set temperatures")
    temp_get.add_argument("--json", action="store_true", help="emit raw JSON")

    temp_set = temp_sub.add_parser("set", help="set target temperature")
    temp_set.add_argument("value", type=float, help="temperature value")
    temp_set.add_argument("--unit", choices=["F", "C", "f", "c"], help="override configured unit")
    temp_set.add_argument("--json", action="store_true", help="emit raw JSON")

    return parser


def _handle_error(exc: Exception) -> int:
    print(f"hottubctl error: {exc}", file=sys.stderr)
    return 2


def cmd_spas(as_json: bool) -> int:
    try:
        spas = asyncio.run(list_spas())
    except (ConfigError, SpaSelectionError, RuntimeError, ValueError) as exc:
        return _handle_error(exc)

    if as_json:
        print(json.dumps(spas, indent=2, sort_keys=True))
        return 0

    for spa in spas:
        print(f"- {spa['name']} ({spa['brand']} {spa['model']}) [{spa['id']}]")
    return 0


def cmd_temp_get(as_json: bool) -> int:
    try:
        status = asyncio.run(get_temperature_status())
    except (ConfigError, SpaSelectionError, RuntimeError, ValueError) as exc:
        return _handle_error(exc)

    if as_json:
        print(json.dumps(status, indent=2, sort_keys=True))
        return 0

    print(f"Spa: {status['spa_name']} ({status['spa_id']})")
    print(f"Water: {status['water_temp_display']}")
    print(f"Set:   {status['set_temp_display']}")
    if status.get('heat_mode'):
        print(f"Heat mode: {status['heat_mode']}")
    return 0


def cmd_temp_set(value: float, unit: str | None, as_json: bool) -> int:
    try:
        result = asyncio.run(set_temperature(value, unit))
    except (ConfigError, SpaSelectionError, RuntimeError, ValueError) as exc:
        return _handle_error(exc)

    if as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print(f"Spa: {result['spa_name']} ({result['spa_id']})")
    print(f"Set temperature: {result['set_temp_display']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "spas":
        return cmd_spas(args.json)
    if args.command == "temp":
        if args.temp_command == "get":
            return cmd_temp_get(args.json)
        if args.temp_command == "set":
            return cmd_temp_set(args.value, args.unit, args.json)

    parser.print_help()
    return 1
