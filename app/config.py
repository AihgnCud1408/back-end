import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    db_host: str = os.getenv("DB_HOST")
    db_port: int = int(os.getenv("DB_PORT"))
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_name: str = os.getenv("DB_NAME")
    jwt_secret: str = os.getenv("JWT_SECRET_KEY", "phmizXVVwq0iD_ERfDRrnGohu9l4dOP-3aIb5nrLW_Uv30SdgNYENKJXild-bjDgnDrO-nDyIW4eOkjxVm1jjQ")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expire: int = int(os.getenv("JWT_EXPIRE", 3600))
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqps://jnekdnuc:NLuPT1K2iYu-GRHNp7rpKQMe9c0IYBV-@fuji.lmq.cloudamqp.com/jnekdnuc")

    class Config:
        env_file = "/.env"
        env_file_encoding = "utf-8"

config = Config()
