from time import sleep

from .external.requests_vk import get_newsfeed
from .external.kafka import kafka_client
from .settings import settings

from loguru import logger


async def crawl_vk_newsfeed(task: dict) -> None:
    q = task.get("q", "")
    start_time = task.get("start_time", "")

    logger.info(f"Start crawling by topic {q}")

    newsfeed = await get_newsfeed(q, int(start_time))

    response = newsfeed.get("response", {})
    newsfeed_items = response.get("items", [])

    for news in newsfeed_items:
        prepared_news = {
            "title": news.get("title", ""),
            "description": news.get("text", ""),
            "date": news.get("date", ""),
            "source": settings.crawl_tag,
            "tags": q,
        }

        logger.info(prepared_news)

        kafka_client.producer.send(settings.kafka_producer_topic, value=prepared_news)
        sleep(0.01)
