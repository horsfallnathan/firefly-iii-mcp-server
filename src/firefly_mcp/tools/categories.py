"""Category provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.categories import (
    create_category, 
    delete_category, 
    get_category, 
    list_categories, 
    update_category,
    list_category_transactions,
    list_category_attachments
)
from firefly_mcp.models.model import CategoryArray, CategorySingle, Category, TransactionArray, AttachmentArray
from firefly_mcp.models.requests import (
    CategoryGetRequest, 
    CategoryListRequest, 
    CategoryUpdateRequest,
    CategoryTransactionsRequest,
    CategoryAttachmentsRequest,
    CategoryDeleteRequest,
    CategoryDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
CATEGORY_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all categories. Can be filtered and paginated.",
        "request_model": CategoryListRequest,
        "response_model": CategoryArray,
        "core_function": list_categories,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific category by ID.",
        "request_model": CategoryGetRequest,
        "response_model": CategorySingle,
        "core_function": get_category,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new category.",
        "request_model": Category,
        "response_model": CategorySingle,
        "core_function": create_category,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing category.",
        "request_model": CategoryUpdateRequest,
        "response_model": CategorySingle,
        "core_function": update_category,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a category.",
        "request_model": CategoryDeleteRequest,
        "response_model": CategoryDeleteResponse,
        "core_function": delete_category,
        "tags": {"write", "delete"}
    },
    
    "list_transactions": {
        "description": "List all transactions in a category, optionally limited to date ranges.",
        "request_model": CategoryTransactionsRequest,
        "response_model": TransactionArray,
        "core_function": list_category_transactions,
        "tags": {"read", "list", "transactions", "pagination"}
    },
    
    "list_attachments": {
        "description": "List all attachments for a category.",
        "request_model": CategoryAttachmentsRequest,
        "response_model": AttachmentArray,
        "core_function": list_category_attachments,
        "tags": {"read", "list", "attachments", "pagination"}
    }
}


def create_category_provider():
    """Factory function to create the category provider with simplified configuration."""
    return create_provider_from_config(EntityType.CATEGORY, CATEGORY_OPERATIONS)

category_provider = create_category_provider()
