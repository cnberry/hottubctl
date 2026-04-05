# AGENTS.md

## What this repo is

`hottubctl` is a terminal-first Sundance SmartTub control project.

The goal is to build:
- a clean library layer
- a sharp CLI
- small, explicit commands
- enough SmartTub understanding to inspect and control a real spa honestly

Think: UNIX tool, not spa-lifestyle app sludge.

## Project principles

- **Library first, CLI immediately useful.**
  The API/control logic should be reusable, while the CLI stays pleasant for direct human use.

- **Be honest about freshness.**
  If the spa is offline or the telemetry is stale, say so plainly.

- **Small commands, low surprise.**
  Commands should do one thing well and print useful output.

- **Read before write, then add guarded writes.**
  Prove inspection flows first, then extend mutating commands carefully.

- **Update docs when the shape settles.**
  When a change feels right, update `README.md` and `AGENTS.md` in the same stretch of work.

- **Prefer pipx for installed CLI usage.**
  For daily use, these tools should behave like normal commands on the user path. Reserve local venv activation for development and testing.

## Current shape

- `hottubctl/smarttub_api.py` — SmartTub login and spa selection helpers
- `hottubctl/temperature.py` — temperature read/set logic plus freshness interpretation
- `hottubctl/render.py` — human-readable status rendering
- `hottubctl/config.py` — local config lookup outside the repo by default
- `hottubctl/cli.py` — command-line entrypoint
- `research.md` — API notes and rough edges discovered so far

`SKILL.md` should live at the repo root so agent workflows can drive this CLI directly.

## Near-term roadmap

1. Keep the current temp/status commands sharp and boring
2. Add more status surfaces only if they stay readable
3. Improve structured JSON output where useful
4. Keep the install/reinstall workflow clean via `pipx`
5. Grow feature-by-feature from proven working commands

## Style

- Keep code boring and readable.
- Avoid needless framework energy.
- Prefer explicit names over magic.
- Don’t let the repo turn into glossy smart-home cosplay.

## Vibe

This project is a small terminal soak for checking whether the tub is actually telling the truth.

♨️🤖🛁
