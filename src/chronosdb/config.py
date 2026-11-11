"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the API and Db2 connection."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    app_env: str = Field(default="development", validation_alias="APP_ENV")
    app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    schema_version: str = Field(default="0", validation_alias="SCHEMA_VERSION")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    db2_host: str = Field(default="localhost", validation_alias="DB2_HOST")
    db2_port: int = Field(default=50000, validation_alias="DB2_PORT", gt=0, le=65535)
    db2_database: str = Field(default="", validation_alias="DB2_DATABASE")
    db2_username: str = Field(default="", validation_alias="DB2_USERNAME")
    db2_password: str = Field(default="", validation_alias="DB2_PASSWORD")
    db2_schema: str = Field(default="", validation_alias="DB2_SCHEMA")
    db2_connect_timeout_seconds: int = Field(
        default=5,
        validation_alias="DB2_CONNECT_TIMEOUT_SECONDS",
        gt=0,
        le=60,
    )

    @property
    def db2_configured(self) -> bool:
        """Return whether all required Db2 connection values are present."""

        return all(
            (
                self.db2_host.strip(),
                self.db2_database.strip(),
                self.db2_username.strip(),
                self.db2_password.strip(),
                self.db2_schema.strip(),
            )
        )

    def connection_dsn(self) -> str:
        """Build a Db2 DSN without including credentials in the returned value."""

        return (
            f"DATABASE={self.db2_database};"
            f"HOSTNAME={self.db2_host};"
            f"PORT={self.db2_port};"
            "PROTOCOL=TCPIP;"
            f"CURRENTSCHEMA={self.db2_schema};"
            f"CONNECTTIMEOUT={self.db2_connect_timeout_seconds};"
        )


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide immutable configuration instance."""

    return Settings()
