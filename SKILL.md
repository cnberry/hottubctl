---
name: hottubctl
description: Control a Sundance SmartTub spa from the local `hottubctl` CLI. Use when asked to list spas, check spa status or temperature freshness, read set/current temperature, or set target temperature from this repo.
---

# hottubctl

Use the local `hottubctl` CLI from this repository.

## Rules

- Prefer the `hottubctl` CLI over ad-hoc Python when the command already exists.
- Keep responses short and action-oriented.
- Report compact final CLI output, not raw internal debugging unless asked.
- Be explicit when SmartTub reports the spa offline or the telemetry looks stale.

## Run from repo root

Preferred daily-use flow:

```bash
cd /home/chris/.openclaw/workspace/hottubctl
hottubctl temp get
```

Local config is expected at one of:
- `$HOTTUBCTL_CONFIG`
- `~/.config/hottubctl/hottubctl.json`
- `~/.hottubctl/hottubctl.json`

## Command map

### Inspection

```bash
hottubctl spas
hottubctl temp get
```

### Control

```bash
hottubctl temp set 101
```

Use for requests like:
- "what temp is the hot tub?"
- "is the spa online?"
- "is this stale SmartTub data?"
- "set the hot tub to 101"

## Response style

Examples:
- "Hot tub is offline; displayed temperatures appear stale."
- "Set temperature: 101°F"
- "Spa: Example Spa — Water: 101.5°F, Set: 102.0°F"

If a command fails, quote the relevant error briefly and say what you’ll do next.
