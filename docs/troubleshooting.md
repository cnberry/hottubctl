# Troubleshooting

## Config is not found

Create `~/.config/hottubctl/hottubctl.json` from the public example, keep it mode
`0600`, set `HOTTUBCTL_PASSWORD` from a password manager, or set
`HOTTUBCTL_CONFIG` to an explicit private file. Repository-local credential
files are intentionally unsupported.

## Multiple spas are found

Add an exact `spa_name` or `spa_id` to the private config. The CLI refuses to
guess among several spas.

## The spa is offline

SmartTub may still return last-known temperatures. Read the connectivity and
timestamp lines together, and do not interpret old values as live physical
state. Confirm through the official or physical control path if needed.

## A write is refused

Temperature writes require `--yes`. Re-run only after checking the selected spa,
numeric value, unit, and physical safety.

## Login or API behavior changes

Upgrade and test `python-smarttub` in a branch, inspect upstream release notes,
and keep credentials out of logs. Do not repeatedly retry authentication in a
tight loop.
