"""Piggy Bank provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.piggy_banks import (
    create_piggy_bank, 
    delete_piggy_bank, 
    get_piggy_bank, 
    list_piggy_banks, 
    update_piggy_bank,
    list_piggy_bank_events,
    list_piggy_bank_attachments
)
from firefly_mcp.models.model import PiggyBankArray, PiggyBankSingle, PiggyBankStore, PiggyBankEventArray, AttachmentArray
from firefly_mcp.models.requests import (
    PiggyBankGetRequest, 
    PiggyBankListRequest, 
    PiggyBankUpdateRequest,
    PiggyBankEventsRequest,
    PiggyBankAttachmentsRequest,
    PiggyBankDeleteRequest,
    PiggyBankDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
PIGGY_BANK_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all piggy banks. Can be filtered and paginated.",
        "request_model": PiggyBankListRequest,
        "response_model": PiggyBankArray,
        "core_function": list_piggy_banks,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific piggy bank by ID.",
        "request_model": PiggyBankGetRequest,
        "response_model": PiggyBankSingle,
        "core_function": get_piggy_bank,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new piggy bank.",
        "request_model": PiggyBankStore,
        "response_model": PiggyBankSingle,
        "core_function": create_piggy_bank,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing piggy bank.",
        "request_model": PiggyBankUpdateRequest,
        "response_model": PiggyBankSingle,
        "core_function": update_piggy_bank,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a piggy bank.",
        "request_model": PiggyBankDeleteRequest,
        "response_model": PiggyBankDeleteResponse,
        "core_function": delete_piggy_bank,
        "tags": {"write", "delete"}
    },
    
    "list_events": {
        "description": "List all events linked to a piggy bank (adding and removing money).",
        "request_model": PiggyBankEventsRequest,
        "response_model": PiggyBankEventArray,
        "core_function": list_piggy_bank_events,
        "tags": {"read", "list", "events", "pagination"}
    },
    
    "list_attachments": {
        "description": "List all attachments for a piggy bank.",
        "request_model": PiggyBankAttachmentsRequest,
        "response_model": AttachmentArray,
        "core_function": list_piggy_bank_attachments,
        "tags": {"read", "list", "attachments", "pagination"}
    }
}


def create_piggy_bank_provider():
    """Factory function to create the piggy bank provider with simplified configuration."""
    return create_provider_from_config(EntityType.PIGGY_BANK, PIGGY_BANK_OPERATIONS)

piggy_bank_provider = create_piggy_bank_provider()
