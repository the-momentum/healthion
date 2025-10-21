from fastmcp import FastMCP, Client
from fastmcp.server.auth.providers.auth0 import Auth0Provider

from app.config import settings

client = Client("http://localhost:8070/mcp/", auth=Auth0Provider(
    config_url=settings.auth0_config_url,
    client_id=settings.auth0_client_id,
    client_secret=settings.auth0_client_secret.get_secret_value(),
    audience=settings.auth0_audience,
    base_url=settings.base_url,
    redirect_path=settings.auth0_redirect_path,
))

proxy = FastMCP.as_proxy(client, name="Healthion MCP Proxy")

if __name__ == "__main__":
    proxy.run()