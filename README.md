# hottubctl ♨️🤖🛁

A terminal-first Sundance SmartTub control tool for checking spa state without poking around a glossy phone app.

`hottubctl` is the spa-shaped member of the same little CLI family as `poolctl` and `lightctl`: small commands, readable output, and local config instead of repo-shaped secrets.

## What it does

- lists SmartTub-visible spas
- shows current water/set temperature
- shows SmartTub connectivity state (`ONLINE` / `OFFLINE`)
- warns when telemetry appears stale
- sets target temperature

## Install

```bash
git clone git@github.com:your-user/hottubctl.git
cd hottubctl
just install
```

That installs `hottubctl` with `pipx` so it behaves like a normal command on your path.

Useful `just` targets:

```bash
just status
just spas
just temp-get
just temp-set 101
```

## Local config

`hottubctl` looks for config in this order:
- `$HOTTUBCTL_CONFIG`
- `~/.config/hottubctl/hottubctl.json`
- `~/.hottubctl/hottubctl.json`
- repo-local `config/hottubctl.json` (dev-only fallback)

Start from:
- `config/hottubctl.example.json`

Expected fields:
- SmartTub username/email
- SmartTub password
- optional preferred spa name or spa id
- preferred temperature unit

Do **not** commit real credentials.

## Commands

- `hottubctl spas`
- `hottubctl temp get`
- `hottubctl temp set 101`

`temp get` reports:
- water temperature
- set temperature
- heat mode when available
- connectivity check time
- telemetry age
- water reading age
- a freshness note when the spa appears offline and the data may be stale

## Development

For early API exploration or proof-of-life work:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python hottubctl.py spas
python hottubctl.py temp get
```

Once the idea is working, prefer the installed command shape via `just install` / `just reinstall`.

## Why this repo exists

The goal is simple: make the useful spa checks fast, scriptable, and honest about freshness.
If the tub is offline, the CLI should say so instead of pretending stale numbers are live truth.

## Extra docs

- `config/hottubctl.example.json` — starter example config
- `research.md` — API notes and rough edges discovered so far
