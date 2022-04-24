import httpx
from loguru import logger

from ...settings import settings


async def get_currencies_rate() -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            settings.cbr_link,
        )

        if not resp:
            logger.info("No data")
            return {}

        return resp.json()
