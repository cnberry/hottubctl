# Roadmap

## Proven surface

- private SmartTub account configuration
- spa listing and unambiguous selection
- online/offline and temperature status
- separate telemetry and water-reading freshness
- guarded target-temperature writes with post-write readback
- human and JSON output

## Next

- mock SmartTub login, spa selection, reads, writes, and session cleanup;
- add stable JSON-schema notes and error categories;
- validate dependency updates across supported Python versions;
- document supervised behavior across additional spa models.

## Research track

- identify exact controller families and evidence for local equipment-bus reads;
- keep experimental local transport separate from the proven cloud commands;
- require model-specific safety analysis before any local write surface.

## Out of scope by default

- unattended safety-critical automation;
- repository-local credentials or public account identifiers;
- claiming water reached a target from cloud setpoint acknowledgement alone;
- generic control of unvalidated spa equipment.
