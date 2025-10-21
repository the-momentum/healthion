from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / "envs" / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        # default env_file solution search .env every time BaseSettings is instantiated
        # dotenv search .env when module is imported, without usecwd it starts from the file it was called
    )

    # API SETTINGS
    api_name: str = f"healthion-mcp API"
    api_v1: str = "/api/v1"
    api_latest: str = api_v1
    paging_limit: int = 100

    # External API settings for healthion-api
    healthion_api_base_url: str
    healthion_api_access_token: SecretStr | None


    # MCP SETTINGS
    mcp_server_name: str = f"MCP Server"

    # AUTH0 SETTINGS
    auth0_config_url: str
    auth0_client_id: str
    auth0_client_secret: SecretStr | None = None
    auth0_audience: str
    base_url: str = "http://localhost:8070"  # Your FastMCP server URL
    auth0_redirect_path: str = "/auth/callback"


    # 0. pytest ini_options
    # 1. environment variables
    # 2. .env
    # 3. default values in pydantic settings


@lru_cache()
def _get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = _get_settings()
