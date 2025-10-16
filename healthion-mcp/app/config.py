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
    api_name: str = f"healthion-mcp API"
    api_v1: str = "/api/v1"
    api_latest: str = api_v1
    paging_limit: int = 100

    # External API settings for healthion-api
    healthion_api_base_url: str = "https://backend-production-d015.up.railway.app"
    healthion_api_access_token: SecretStr | None = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlzRW8yTXh0eWloaGQtVVowZmQtNiJ9.eyJpc3MiOiJodHRwczovL2Rldi10NXFsMm1xcWMwZ2s0ams2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExNjU4MzY2OTI2NDUzNDkwNjQ4NSIsImF1ZCI6WyJodHRwczovL2Rldi10NXFsMm1xcWMwZ2s0ams2LnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kZXYtdDVxbDJtcXFjMGdrNGprNi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzYwNTM1ODQzLCJleHAiOjE3NjA2MjIyNDMsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MiLCJhenAiOiJkR1NVMGdUWW5FVlBzR2ZkTk1rVlloTXlrOEIzMDFNbCJ9.SXn2eow28aGEAwxSRe1dRmtSCQXxguouJ5GJLBl3b1Ej1OSsMPk2KX6sLVjdTTB89db-eqiBzegNPrb4K-klfn0PnzQTxCRM5-pqkkCwnzA0Ivb7PgGs6Vtsw8sXXOCu-rmuFUa1FD9jRDpzLZYkzbLkV028JIsYMywBsaWYcosHzS16k3-wXwlYaYlHPtDGmiG1OSF5sEqDEMMIJ9DGUFFhAlF_r7wv5xGFqvo1HP-9pRZuo7A4EcULMV0V-WQ5H242Tnmegs8SkaFgsPRF_MG6NjG6yqA1IxRWctvq6JG0HlIXolZ7G-amLeZB5ya9GSk5pmPkiwSMdqiF8rE49Q"



    # MCP SETTINGS
    mcp_server_name: str = f"MCP Server"


    # 0. pytest ini_options
    # 1. environment variables
    # 2. .env
    # 3. default values in pydantic settings


@lru_cache()
def _get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = _get_settings()
