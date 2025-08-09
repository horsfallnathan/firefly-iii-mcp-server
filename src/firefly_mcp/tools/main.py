"""Main entry point for the Firefly III MCP server."""

from contextlib import AbstractAsyncContextManager
from typing import Callable
from fastmcp import FastMCP

from firefly_mcp.models.app import AppContext
from firefly_mcp.tools.accounts import account_provider
from firefly_mcp.tools.bills import bill_provider
from firefly_mcp.tools.budgets import budget_provider
from firefly_mcp.tools.categories import category_provider
from firefly_mcp.tools.piggy_banks import piggy_bank_provider
from firefly_mcp.tools.rule_groups import rule_group_provider
from firefly_mcp.tools.rules import rule_provider
from firefly_mcp.tools.tags import tag_provider
from firefly_mcp.tools.transactions import transaction_provider
from firefly_mcp.tools.registry import setup_firefly_tools
from firefly_mcp.tools.utils import register_version_tool, register_echo_tool
# from fastmcp.server.middleware import Middleware, MiddlewareContext

# class LoggingMiddleware(Middleware):
#     async def on_message(self, context: MiddlewareContext, call_next):
#         print(f"-> Received {context.method}")
#         result = await call_next(context)
#         print(f"<- Responded to {context.method}")
#         return result
    
def create_mcp_server(lifespan: Callable[[FastMCP], AbstractAsyncContextManager[AppContext, bool | None]] | None = None) -> FastMCP:
    """Create and configure the FastMCP server with consolidated Firefly III tools."""
    if lifespan is not None:
        mcp = FastMCP("Firefly MCP Server", lifespan=lifespan)
    else:
        mcp = FastMCP("Firefly MCP Server")

    # Register the Firefly III tools
    providers = [account_provider, bill_provider, budget_provider, category_provider, piggy_bank_provider, rule_group_provider, rule_provider, tag_provider, transaction_provider]
    setup_firefly_tools(mcp, providers)
    
    # Register utility tools
    register_version_tool(mcp)
    register_echo_tool(mcp)

    # mcp.add_middleware(LoggingMiddleware())
    return mcp