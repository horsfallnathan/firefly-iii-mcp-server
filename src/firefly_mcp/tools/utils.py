"""Utility functions for Firefly MCP tools."""

from typing import TypeVar
from fastmcp import FastMCP
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


def register_version_tool(mcp: FastMCP) -> None:
    """Register the version tool."""
    @mcp.tool(
        name="get_version",
        description="Get the version of the Firefly MCP server",
    )
    def version_tool(random_string: str = "dummy") -> str: # type: ignore[reportUnusedFunction]
        """Get the current version of the server."""
        return "1.0.0"


def register_echo_tool(mcp: FastMCP) -> None:
    """Register the echo tool."""
    @mcp.tool(
        name="echo",
        description="Echo a message back to the user",
    )
    def echo_tool(message: str) -> str:  # type: ignore[reportUnusedFunction]
        """Echo the provided message back to the user."""
        return message 