import httpx
from loguru import logger

from ...settings import settings


async def get_newsfeed(q: str, start_time: int) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            settings.vk_api_link_newsfeed,
            params={
                "count": 10,
                "access_token": settings.vk_api_access_token,
                "v": settings.vk_api_v,
                "q": q,
                "start_time": start_time,
            },
        )

        if not resp:
            logger.info("No data")
            return {}

        return resp.json()
