from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_host: str
    kafka_port: int
    kafka_consumer_topic: str
    kafka_consumer_group: str
    kafka_producer_topic: str

    vk_api_link_newsfeed: str
    vk_api_v: str
    vk_api_access_token: str

    crawl_tag: str = "VK"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
