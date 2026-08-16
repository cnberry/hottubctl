# Operations and safety

## Read before write

Use `hottubctl spas` and `hottubctl temp get` before a write when the selected
spa, unit, or current state is unclear. Temperature writes require `--yes`; the
flag confirms intent, not physical safety.

## Temperature write sequence

`hottubctl temp set VALUE --yes`:

1. loads the private account configuration;
2. logs in through `python-smarttub`;
3. selects an exact configured spa, or the account's only spa;
4. converts Fahrenheit input to Celsius when needed;
5. sends the target temperature;
6. reads spa status again; and
7. reports the target value returned by SmartTub.

The returned setpoint confirms cloud/API state, not current water temperature.
Use `temp get` and physical controls for follow-up verification.

## Stale data

Connectivity status and temperature telemetry can have different timestamps.
When the spa is offline, temperatures may be last-known values. The CLI reports
their available ages and adds an explicit freshness note instead of treating
them as live.

## Live validation

Automated tests never log in or perform writes. Before a release that changes
write behavior, validate a supervised read, a small safe setpoint change, the
returned target, and a restore to the original target.
