from __future__ import annotations

import aiohttp
from smarttub import SmartTub

from .config import preferred_spa_selector, smarttub_credentials


class SpaSelectionError(RuntimeError):
    pass


async def login_client() -> SmartTub:
    username, password = smarttub_credentials()
    session = aiohttp.ClientSession()
    client = SmartTub(session)
    try:
        await client.login(username, password)
    except Exception:
        await session.close()
        raise
    return client


async def select_spa(client: SmartTub):
    account = await client.get_account()
    spas = await account.get_spas()
    spa_name, spa_id = preferred_spa_selector()

    if spa_id:
        for spa in spas:
            if spa.id == spa_id:
                return spa
        raise SpaSelectionError(f"preferred spa_id '{spa_id}' not found")

    if spa_name:
        for spa in spas:
            if spa.name == spa_name:
                return spa
        raise SpaSelectionError(f"preferred spa_name '{spa_name}' not found")

    if len(spas) == 1:
        return spas[0]

    raise SpaSelectionError(
        "multiple spas found; set spa_name or spa_id in the private hottubctl config"
    )
