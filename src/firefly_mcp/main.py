import logging

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP
from firefly_mcp.tools.main import create_mcp_server
from firefly_mcp.models.app import AppContext

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context."""
    # Initialize on startup
    logging.info("Starting up...")
    try:
        yield AppContext()
    finally:
        logging.info("Shutting down...")

mcp = create_mcp_server(app_lifespan)

def get_mcp_server() -> FastMCP:
    """Get the configured MCP server instance."""
    return mcp
def main():
    """Main entry point for the MCP server."""

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
