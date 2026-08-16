# Protocol notes

`hottubctl` uses `python-smarttub` and `aiohttp` to access the SmartTub cloud.
It does not directly speak to the spa over the local network. The client logs in
for each command, selects a spa from the account, performs the requested read or
write, and closes its HTTP session.

The public CLI exposes spa listing and temperature status/set only. SmartTub may
return connectivity, telemetry, and individual water-reading timestamps with
different ages; these are preserved separately in structured output.

A local-control path may be possible for some Sundance/Jacuzzi controller
families through their equipment bus, but hardware compatibility and safe write
semantics are not established here. That investigation should remain separate
from the proven cloud CLI until it has model-specific evidence and supervised
validation.
