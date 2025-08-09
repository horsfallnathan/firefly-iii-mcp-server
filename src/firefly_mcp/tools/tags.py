"""Tag provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.tags import (
    get_tag, list_tags, create_tag, update_tag, delete_tag,
    list_tag_transactions, list_tag_attachments
)
from firefly_mcp.models.model import (
    TagArray, TagSingle, TagModelStore, TransactionArray, AttachmentArray
)
from firefly_mcp.models.requests import (
    TagGetRequest, TagListRequest, TagUpdateRequest,
    TagTransactionsRequest, TagAttachmentsRequest, TagDeleteRequest, TagDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
TAG_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all tags. Can be filtered and paginated.",
        "request_model": TagListRequest,
        "response_model": TagArray,
        "core_function": list_tags,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific tag by ID.",
        "request_model": TagGetRequest,
        "response_model": TagSingle,
        "core_function": get_tag,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new tag.",
        "request_model": TagModelStore,
        "response_model": TagSingle,
        "core_function": create_tag,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing tag.",
        "request_model": TagUpdateRequest,
        "response_model": TagSingle,
        "core_function": update_tag,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a tag.",
        "request_model": TagDeleteRequest,
        "response_model": TagDeleteResponse,
        "core_function": delete_tag,
        "tags": {"write", "delete"}
    },
    
    "list_transactions": {
        "description": "List all transactions for a tag, optionally limited to date ranges.",
        "request_model": TagTransactionsRequest,
        "response_model": TransactionArray,
        "core_function": list_tag_transactions,
        "tags": {"read", "list", "transactions", "pagination"}
    },
    
    "list_attachments": {
        "description": "List all attachments for a tag.",
        "request_model": TagAttachmentsRequest,
        "response_model": AttachmentArray,
        "core_function": list_tag_attachments,
        "tags": {"read", "list", "attachments", "pagination"}
    }
}


def create_tag_provider():
    """Factory function to create the tag provider with simplified configuration."""
    return create_provider_from_config(EntityType.TAG, TAG_OPERATIONS)

tag_provider = create_tag_provider()