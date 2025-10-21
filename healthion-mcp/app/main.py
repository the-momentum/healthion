from logging import INFO, basicConfig

from fastmcp import FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider

from app.config import settings
from app.mcp import mcp_router

basicConfig(level=INFO, format="[%(asctime)s - %(name)s] (%(levelname)s) %(message)s")

auth = Auth0Provider(
    config_url=settings.auth0_config_url,
    client_id=settings.auth0_client_id,
    client_secret=settings.auth0_client_secret.get_secret_value(),
    audience=settings.auth0_audience,
    base_url=settings.base_url,
    redirect_path=settings.auth0_redirect_path,
)

mcp = FastMCP(name=settings.mcp_server_name, auth=auth)


mcp.mount(mcp_router)
