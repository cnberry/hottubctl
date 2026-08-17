# Repository guidance

## Purpose

`hottubctl` is a terminal-first Sundance SmartTub inspection and control tool.
Keep cloud/API handling, temperature logic, rendering, and CLI dispatch
separate, and be precise about whether data is live or last-known.

## Engineering principles

- Treat offline or old telemetry as stale, not as current physical truth.
- Keep commands small, explicit, and scriptable.
- Treat heated water equipment as safety-sensitive.
- Require a deliberate guard for every mutating command.
- Report post-write state instead of equating request acceptance with success.
- Keep real credentials, spa names, and identifiers outside the public repo.
- Preserve compact human output and stable JSON output.
- Test conversion, freshness, rendering, configuration, selection, and CLI
  guards without requiring a live SmartTub account.
- Update `README.md`, `SKILL.md`, and relevant files under `docs/` when command
  behavior changes.
- Maintain `script/install` as the language-neutral deployment contract. A
  future Rust migration changes that script, not private bootstrap callers.

## Layout

- `hottubctl/smarttub_api.py` — login and exact spa selection
- `hottubctl/temperature.py` — temperature reads, writes, and freshness logic
- `hottubctl/render.py` — human-readable status rendering
- `hottubctl/config.py` — private local account configuration
- `hottubctl/cli.py` — command-line parser and dispatch
- `script/install` — stable installer entry point for deployment automation
- `tests/` — account-free unit tests
- `docs/` — operations, protocol, troubleshooting, and roadmap notes

## Development

Use the private home-ops bootstrap for installed use and `.venv` for development. Run the full
format, lint, secret-scan, and test sequence documented in `README.md` before
publishing. Never perform a live spa write as part of an automated test.
