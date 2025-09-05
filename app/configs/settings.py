import os
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class GeneralSettings(BaseSettings):
    TIMEZONE: str = "Asia/Kolkata"
    SECRET_KEY: str = "Mh1A0qIy96Cztb27yRL_UfliYp1RKOactcSpI1Ojf8Y"
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: str = "30"
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: str = "7"
    DASHBOARD_APP_URL: str = "http://localhost:5173"


class DatabaseSettings(BaseSettings):
    MONGODB_URI: str = os.environ.get("MONGODB_URI")
    DB_NAME: str = os.environ.get("DB_NAME")


class CloudinarySettings(BaseSettings):
    CLOUD_NAME: str = os.environ.get("CLOUD_NAME")
    API_KEY: str = os.environ.get("API_KEY")
    API_SECRET: str = os.environ.get("API_SECRET")
    GALLERY_FOLDER_NAME: str = os.environ.get("GALLERY_FOLDER_NAME")


class EmailSettings(BaseSettings):
    MAIL_RECEIVER: str = os.environ.get("MAIL_RECEIVER")
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM: str = os.environ.get("MAIL_FROM")
    MAIL_PORT: int = os.environ.get("MAIL_PORT")
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.environ.get("MAIL_FROM_NAME")
    MAIL_STARTTLS: bool = os.environ.get("MAIL_STARTTLS")
    MAIL_SSL_TLS: bool = os.environ.get("MAIL_SSL_TLS")
    USE_CREDENTIALS: bool = os.environ.get("USE_CREDENTIALS")
    VALIDATE_CERTS: bool = os.environ.get("VALIDATE_CERTS")


class Settings(DatabaseSettings, CloudinarySettings, EmailSettings, GeneralSettings):
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
