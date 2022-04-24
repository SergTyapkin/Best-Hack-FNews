from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    token_expires_in_secs: int = 1800
    jwt_tokens_aud: str = "auth"
    jwt_algorithm: str = "HS256"
    jwt_tokens_prefix: str = "Bearer"
    token_issuer: str = "best-hack.io"
    secret_key: str

    cbr_link: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
