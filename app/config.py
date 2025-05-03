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
    jwt_secret: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    jwt_expire: int = int(os.getenv("JWT_EXPIRE"))
    smtp_host: str = os.getenv("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT"))
    smtp_user: str = os.getenv("SMTP_USER")
    smtp_password: str = os.getenv("SMTP_PASSWORD")
    email_from: str = os.getenv("EMAIL_FROM")

    class Config:
        env_file = "/.env"
        env_file_encoding = "utf-8"

config = Config()
