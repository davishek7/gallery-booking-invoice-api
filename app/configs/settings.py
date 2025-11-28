import os
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class GeneralSettings(BaseSettings):
    TIMEZONE: str = "Asia/Kolkata"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: str = os.environ.get("ACCESS_TOKEN_EXPIRE_TIMEDELTA")
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: str = os.environ.get(
        "REFRESH_TOKEN_EXPIRE_TIMEDELTA"
    )
    FRONTEND_APP_URL: str = os.environ.get("FRONTEND_APP_URL")
    ADMIN_APP_URL: str = os.environ.get("ADMIN_APP_URL")
    ALLOW_REGISTRATION: str = os.environ.get("ALLOW_REGISTRATION")


class DatabaseSettings(BaseSettings):
    MONGODB_URI: str = os.environ.get("MONGODB_URI")
    DB_NAME: str = os.environ.get("DB_NAME")


class CloudinarySettings(BaseSettings):
    CLOUD_NAME: str = os.environ.get("CLOUD_NAME")
    API_KEY: str = os.environ.get("API_KEY")
    API_SECRET: str = os.environ.get("API_SECRET")


class SupabaseSettings(BaseSettings):
    SUPABASE_KEY: str = os.environ.get("SUPABSE_KEY")
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL")


class CloudflareR2Settings(BaseSettings):
    R2_ACCESS_KEY_ID: str = os.environ.get("R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY: str = os.environ.get("R2_SECRET_ACCESS_KEY")
    R2_ENDPOINT_URL: str = os.environ.get("R2_ENDPOINT_URL")


class MediaStorageSettings(BaseSettings):
    GALLERY_FOLDER_NAME: str = os.environ.get("GALLERY_FOLDER_NAME")
    INVOICE_FOLDER_NAME: str = os.environ.get("INVOICE_FOLDER_NAME")


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


class Settings(
    DatabaseSettings,
    CloudinarySettings,
    EmailSettings,
    GeneralSettings,
    SupabaseSettings,
    CloudflareR2Settings,
    MediaStorageSettings,
):
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
