from functools import lru_cache
from typing import List, Set

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.config"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    python_env: str = "dev"
    app_name: str = "CCODEL Tickets"
    app_url: str = "http://localhost:5173"
    frontend_urls: str = "http://localhost:5173,http://localhost:8000"

    db_url: str = ""
    database_url: str = ""

    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    storage_backend: str = "cloudinary"
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10
    allowed_upload_types: str = (
        "image/jpeg,image/png,image/gif,image/webp,application/pdf,"
        "application/msword,"
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""
    cloudinary_folder: str = "ccodel_tickets"
    cloudinary_private_download_ttl: int = 3600

    mail_enabled: bool = False
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = ""
    mail_port: int = 587
    mail_server: str = ""
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True

    admin_email: str = ""
    admin_password: str = ""
    admin_first_name: str = "Admin"
    admin_last_name: str = "User"
    admin_matric_number: str = ""

    test_database_url: str = ""

    @property
    def sqlalchemy_url(self) -> str:
        return self.db_url or self.database_url

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.frontend_urls.split(",") if origin.strip()]

    @property
    def allowed_mime_types(self) -> Set[str]:
        return {
            mime.strip().lower()
            for mime in self.allowed_upload_types.split(",")
            if mime.strip()
        }

    @property
    def cloudinary_configured(self) -> bool:
        return all(
            [
                self.cloudinary_cloud_name,
                self.cloudinary_api_key,
                self.cloudinary_api_secret,
            ]
        )

    @property
    def mail_configured(self) -> bool:
        return bool(
            self.mail_enabled
            and self.mail_username
            and self.mail_password
            and self.mail_from
            and self.mail_server
        )

    def validate_runtime(self) -> None:
        if not self.sqlalchemy_url:
            raise RuntimeError("DB_URL is not configured")
        if not self.secret_key:
            raise RuntimeError("SECRET_KEY is not configured")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
