from typing import Optional

from kafka import KafkaProducer, KafkaConsumer


class KafkaClient:
    consumer: Optional[KafkaConsumer]
    producer: Optional[KafkaProducer]


kafka_client = KafkaClient()
