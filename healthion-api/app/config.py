from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / "config" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        # default env_file solution search .env every time BaseSettings is instantiated
        # dotenv search .env when module is imported, without usecwd it starts from the file it was called
    )

    # API SETTINGS
    api_name: str = f"healthion-api API"
    api_v1: str = "/api/v1"
    api_latest: str = api_v1
    paging_limit: int = 100

    # DATABASE SETTINGS
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "healthion-api"
    db_user: str = "user"
    db_password: SecretStr = SecretStr("password")



    @property
    def db_uri(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{self.db_password.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # 0. pytest ini_options
    # 1. environment variables
    # 2. .env
    # 3. default values in pydantic settings


@lru_cache()
def _get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = _get_settings()
