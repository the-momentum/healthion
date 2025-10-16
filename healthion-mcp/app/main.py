import sys
from logging import INFO, basicConfig
from pathlib import Path

from fastmcp import FastMCP

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.mcp import mcp_router

basicConfig(level=INFO, format="[%(asctime)s - %(name)s] (%(levelname)s) %(message)s")



mcp = FastMCP(name=settings.mcp_server_name)


mcp.mount(mcp_router)
