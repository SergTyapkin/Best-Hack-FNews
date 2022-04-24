from time import sleep
from loguru import logger
from .external.kafka_utils import connect_to_kafka, close_connection_kafka
from .external.kafka_utils import kafka_client
from .crawler import crawl_vk_newsfeed


async def create_app():
    try:
        connect_to_kafka()

        logger.info("Start listen topic")
        for message in kafka_client.consumer:
            await crawl_vk_newsfeed(message.value)
    except Exception as exc:
        logger.error(exc)
        close_connection_kafka()
