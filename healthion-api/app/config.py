from functools import lru_cache
from pathlib import Path
from enum import Enum

from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / "envs" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API SETTINGS
    api_name: str = "healthion-api API"
    api_v1: str = "/api/v1"
    api_latest: str = api_v1

    paging_limit: int = 100

    debug: bool = False

    environment: EnvironmentType = EnvironmentType.TEST

    backend_cors_origins: list[AnyHttpUrl] = []
    backend_cors_allow_all: bool = False

    # DATABASE SETTINGS
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "healthion-api"
    db_user: str = "user"
    db_password: SecretStr = SecretStr("password")

    # AUTH0 SETTINGS
    auth0_domain: str = ""
    auth0_audience: str = ""
    auth0_issuer: str = ""
    auth0_algorithms: list[str] = ["RS256"]

    @property
    def db_uri(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{self.db_password.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def auth0_issuer_url(self) -> str:
        return f"https://{self.auth0_domain}/"

    # 0. pytest ini_options
    # 1. environment variables
    # 2. .env
    # 3. default values in pydantic settings


@lru_cache()
def _get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = _get_settings()
