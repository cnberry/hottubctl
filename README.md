<p align="center">
  <img src="docs/assets/hottubctl-hero.jpg" alt="Illustration of a terminal monitoring a connected hot tub" width="100%">
</p>

# hottubctl

`hottubctl` is a small Python CLI for inspecting and operating a Sundance
SmartTub spa through the vendor cloud. It lists spas, reports connectivity and
temperature freshness, exposes structured JSON, and performs guarded target-
temperature writes.

> [!WARNING]
> `hottubctl` controls heated water equipment through an unofficial cloud
> integration. Verify the selected spa and requested temperature, preserve a
> working official control path, and do not use stale telemetry as proof that
> the physical equipment is safe.

## What it does

- lists spas visible to the configured SmartTub account;
- reads current water and target temperatures;
- reports online/offline state and the age of available telemetry;
- warns when an offline spa is showing last-known values;
- sets target temperature after an explicit `--yes` guard;
- reads status again and reports the resulting target value.

Python 3.13 or newer is required by the current `python-smarttub` release.

## Install

```bash
git clone https://github.com/cnberry/hottubctl.git
cd hottubctl
./script/install
```

`script/install` is the stable repository contract used by private deployment
automation. Today it installs the Python package with `pipx`; it can be replaced
by a Rust or binary installer later without changing callers. `just install`
uses the same contract.

## Configure private credentials

Install the sanitized example outside the repository, then replace its values:

```bash
mkdir -p ~/.config/hottubctl
install -m 600 config/hottubctl.example.json ~/.config/hottubctl/hottubctl.json
```

Set the password in the process environment before running a command:

```bash
export HOTTUBCTL_PASSWORD='read-from-your-password-manager'
hottubctl temp get
```

The username may come from config or `HOTTUBCTL_USERNAME`; the password may come
from `HOTTUBCTL_PASSWORD` or, for backward compatibility, a mode-`0600` config
field. Optional `spa_name` or `spa_id` selects one spa when the account has
several, and `temperature_unit` accepts `F` or `C`. Set
`HOTTUBCTL_CONFIG=/path/to/hottubctl.json` to use another private file.

Credentials, spa identifiers, and account-specific names belong in a private
configuration repository. Never put them in a public fork, issue, log, or
automation transcript.

## Inspect state

```bash
hottubctl spas
hottubctl temp get
```

Add `--json` after either command for structured output. Human temperature
status includes connectivity time, telemetry age, water-reading age, and a
freshness note when the data may be stale.

## Set target temperature

```bash
hottubctl temp set 101 --yes
hottubctl temp set 38 --unit C --yes
```

The write is refused without `--yes`. The CLI selects the configured spa, sends
the requested setpoint, reads current spa status again, and reports the target
value returned by SmartTub. Cloud confirmation does not prove that the water has
reached that temperature. See [operations](docs/operations.md).

## Runtime data

| Data | Default path | Git policy |
| --- | --- | --- |
| Account/spa config | `~/.config/hottubctl/hottubctl.json` | Private config repo only |
| Password | `HOTTUBCTL_PASSWORD` or legacy config field | Never commit |
| Legacy config | `~/.hottubctl/hottubctl.json` | Private; migrate when practical |
| API responses | Memory and standard output only | Review JSON before sharing |

## Reliability and scope

SmartTub is cloud- and connectivity-dependent. An offline spa may still return
old temperatures, so `hottubctl` reports timestamps and never converts an
offline last-known reading into a claim of current physical state. Vendor API,
authentication, and library behavior can change without notice.

See [protocol notes](docs/protocol.md), [troubleshooting](docs/troubleshooting.md),
and the [roadmap](docs/roadmap.md) for more detail.

## Control-tool family

- [`gatectl`](https://github.com/cnberry/gatectl) — MyQ gate and garage-door
  status with guarded open/close.
- [`poolctl`](https://github.com/cnberry/poolctl) — Pentair ScreenLogic status,
  cleaner, and delay control.
- [`hottubctl`](https://github.com/cnberry/hottubctl) — Sundance SmartTub
  temperature and freshness inspection.
- [`switchctl`](https://github.com/cnberry/switchctl) — named local switch
  status and guarded power control.

Current and future `*ctl` tools favor small commands, private configuration,
readable output, safe JSON, guarded writes, post-write readback, a repo-owned
`script/install`, and explicit uncertainty.

## Development

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/ruff format --check hottubctl tests
.venv/bin/ruff check hottubctl tests
.venv/bin/detect-secrets scan --baseline .secrets.baseline
.venv/bin/pytest -q
```

Automated tests do not log in or contact a real spa. `just test-integration`
does contact the configured account and is deliberately separate.

## License

`hottubctl` is released under the [MIT License](LICENSE).
