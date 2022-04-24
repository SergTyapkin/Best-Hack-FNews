import json

from kafka import KafkaConsumer, KafkaProducer
from loguru import logger

from .kafka import kafka_client
from ...settings import settings
from ...create_app import app

kafka_broker_addr = f"{settings.kafka_host}:{settings.kafka_port}"


@app.on_event("startup")
def connect_to_kafka():
    logger.info("Start kafka connection")
    try:
        # kafka_client.producer = KafkaProducer(
        #     bootstrap_servers=[kafka_broker_addr],
        #     value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        # )
        kafka_client.consumer = KafkaConsumer(
            "vk-crawler-v1",
            bootstrap_servers=[kafka_broker_addr],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=settings.kafka_consumer_group,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )
    except Exception as exc:
        logger.error(exc)
        logger.error("Unable to connect to kafka")


@app.on_event("shutdown")
def close_connection_kafka():
    logger.info("Closing Kafka connection")
    kafka_client.producer.close()
    kafka_client.consumer.close()
