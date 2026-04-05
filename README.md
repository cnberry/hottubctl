# hottubctl

Terminal-first CLI for Sundance SmartTub control.

`hottubctl` is a small CLI focused on the most useful spa operations first:
- read current water temperature
- read set temperature
- set target temperature
- capture enough structure to grow into a proper control tool later

It is modeled after the same boring-tool shape as `poolctl` and `lightctl`.

## Current direction
This repo is scaffolded around the SmartTub cloud API path used by Sundance/Jacuzzi SmartTub-enabled spas.

Research so far indicates:
- login endpoint: `POST https://api.smarttub.io/idp/signin`
- API base: `https://api.smarttub.io`
- account lookup: `GET /accounts/{account_id}`
- spa listing: `GET /spas?ownerId={account_id}`
- spa detail: `GET /spas/{spa_id}`
- status: `GET /spas/{spa_id}/status`
- full status: `GET /spas/{spa_id}/fullStatus`
- set temperature: `PATCH /spas/{spa_id}/config` with JSON body like:
  - `{ "setTemperature": 38.5 }`

Status objects appear to include:
- `setTemperature`
- `water.temperature`
- `displayTemperatureFormat`
- `heatMode`

## CLI shape
Current commands:

```bash
python3 hottubctl.py spas
python3 hottubctl.py temp get
python3 hottubctl.py temp set 101
```

`temp get` now reports:
- explicit SmartTub connectivity state (`ONLINE` / `OFFLINE`)
- when connectivity was last checked
- when telemetry and water readings were last updated
- a freshness note warning when the spa is offline and temperatures may be stale

## Install

```bash
cd REPO_ROOT/hottubctl
just install
```

That installs an editable `hottubctl` command with `pipx`, matching the general pattern used by the other `*ctl` tools.

Useful `just` targets:

```bash
just status
just spas
just temp-get
just temp-set 101
```

## Config
`hottubctl` looks for config in this order:
- `$HOTTUBCTL_CONFIG`
- `~/.config/hottubctl/hottubctl.json`
- `~/.hottubctl/hottubctl.json`
- repo-local `config/hottubctl.json`

Expected fields:
- SmartTub username/email
- SmartTub password or token material
- optional preferred spa name/id
- preferred temperature unit

Do **not** commit real credentials.

## Notes
This is currently cloud-API based research and scaffold work, not proven live control yet. The next milestone is authenticating against the actual SmartTub account and verifying get/set temperature against the real Sundance spa.
