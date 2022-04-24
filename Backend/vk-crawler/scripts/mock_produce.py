from time import sleep
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

producer.send("vk-crawler-v1", value={"q": "Политика", "start_time": "1650736714"})
sleep(1)

# for e in range(1000):
#     data = {"number": e}
#     producer.send("numtest", value=data)
#     sleep(5)

#
