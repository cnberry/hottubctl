# Research notes: Sundance SmartTub

## Most promising integration path
Use the existing SmartTub cloud API rather than starting with packet capture or board-level reverse engineering.

Why:
- there is already a maintained open-source Python client (`python-smarttub`)
- Home Assistant already ships a SmartTub integration, which is a strong signal that account login + control is viable
- the immediate user goal is temperature get/set, which the API already appears to support directly

## Confirmed external findings
Based on `mdz/python-smarttub` and Home Assistant SmartTub docs:

### Authentication
- `POST https://api.smarttub.io/idp/signin`
- JSON body: `{ "username": ..., "password": ... }`
- returns token material including access token and id token
- account id can be derived from JWT payload claim `custom:account_id`

### API base
- `https://api.smarttub.io`

### Account / spa discovery
- `GET /accounts/{account_id}`
- `GET /spas?ownerId={account_id}`
- `GET /spas/{spa_id}`

### Temperature/status path
- `GET /spas/{spa_id}/status`
- `GET /spas/{spa_id}/fullStatus`
- status object appears to include:
  - `setTemperature`
  - `water.temperature`
  - `displayTemperatureFormat`
  - `heatMode`

### Temperature write path
- `PATCH /spas/{spa_id}/config`
- JSON body:
  - `{ "setTemperature": <temp_celsius_rounded_to_1_decimal> }`

Notes from upstream implementation:
- API reportedly returns 500 if temperature has more than one decimal place
- upstream waits for state convergence after writing temperature

## Immediate implementation plan
1. scaffold `hottubctl` CLI repo
2. use `python-smarttub` package as the first backend instead of reimplementing the protocol from scratch
3. support:
   - `spas`
   - `temp get`
   - `temp set`
4. store credentials and preferred spa selector in local config
5. prove against the real account/device

## Open questions for live validation
- exact Sundance spa name/model visible in SmartTub account
- whether the account has only one spa or multiple
- whether set temperature is best handled in F or converted to C at CLI boundary
- whether rate limits or anti-bot protections show up in practice
