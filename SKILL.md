---
name: hottubctl
description: Inspect and control a Sundance SmartTub spa with the hottubctl CLI. Use for spa listing, online state, current and target temperature, telemetry freshness, and guarded target-temperature changes.
---

# hottubctl

Use the installed `hottubctl` CLI instead of ad-hoc cloud calls when a command
already exists.

## Safety rules

- Treat credentials, spa names, identifiers, and raw JSON as private data.
- State plainly when a spa is offline or telemetry may be stale.
- Use `--yes` only after the selected spa, value, and unit are clear.
- Report the target value returned after the write; do not claim the water has
  physically reached it.
- If selection is ambiguous, require private `spa_name` or `spa_id` config
  instead of guessing.

## Commands

```bash
hottubctl spas
hottubctl temp get
hottubctl temp set 101 --yes
hottubctl temp set 38 --unit C --yes
```

Add `--json` for structured output. If a command fails, quote the short error
and do not claim the cloud or equipment reached the requested state.
