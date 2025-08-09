"""Application context models for Firefly MCP server."""

from pydantic import BaseModel


class AppContext(BaseModel):
    """Application context for the Firefly MCP server."""
    
    server_name: str = "Firefly MCP Server"
    version: str = "1.0.0"
    
    model_config = {
        "frozen": True,
        "extra": "forbid",
    }
