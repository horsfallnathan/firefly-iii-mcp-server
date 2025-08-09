"""Schema type definitions for Firefly MCP server operations."""

from typing import Any, Callable, TypedDict, Type
from enum import Enum


class OperationSchema(TypedDict):
    """Type definition for operation schema entries.
    
    This defines the structure of operation schemas used across
    all entity types (accounts, transactions, budgets, etc.).
    Uses flexible typing to accommodate various response and request types.
    """
    response: Any
    request: Any
    description: str
    function: Callable[..., Any]


class EntityRegistrySchema(TypedDict):
    """Type definition for entity registry entries.
    
    This defines the structure of registry entries that map entity types
    to their operation enums and schema functions.
    """
    operations: Type[Enum]
    get_schema: Callable[..., OperationSchema]
