"""Transaction provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.transactions import (
    get_transaction, list_transactions, create_transaction, update_transaction, delete_transaction,
    list_transaction_attachments, list_transaction_piggy_bank_events,
    bulk_categorize_transactions, bulk_tag_transactions
)
from firefly_mcp.models.model import (
    TransactionArray, TransactionSingle, TransactionStore, AttachmentArray, PiggyBankEventArray
)
from firefly_mcp.models.requests import (
    TransactionGetRequest, TransactionListRequest, TransactionUpdateRequest,
    TransactionAttachmentsRequest, TransactionPiggyBankEventsRequest,
    TransactionDeleteRequest, TransactionDeleteResponse,
    BulkCategorizeRequest, BulkTagRequest
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
TRANSACTION_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all transactions. Can be filtered by date range, type, and paginated.",
        "request_model": TransactionListRequest,
        "response_model": TransactionArray,
        "core_function": list_transactions,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific transaction by ID.",
        "request_model": TransactionGetRequest,
        "response_model": TransactionSingle,
        "core_function": get_transaction,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new transaction.",
        "request_model": TransactionStore,
        "response_model": TransactionSingle,
        "core_function": create_transaction,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing transaction.",
        "request_model": TransactionUpdateRequest,
        "response_model": TransactionSingle,
        "core_function": update_transaction,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a transaction.",
        "request_model": TransactionDeleteRequest,
        "response_model": TransactionDeleteResponse,
        "core_function": delete_transaction,
        "tags": {"write", "delete"}
    },
    
    "list_attachments": {
        "description": "List all attachments for a specific transaction.",
        "request_model": TransactionAttachmentsRequest,
        "response_model": AttachmentArray,
        "core_function": list_transaction_attachments,
        "tags": {"read", "list", "attachments", "pagination"}
    },
    
    "list_piggy_bank_events": {
        "description": "List all piggy bank events for a specific transaction.",
        "request_model": TransactionPiggyBankEventsRequest,
        "response_model": PiggyBankEventArray,
        "core_function": list_transaction_piggy_bank_events,
        "tags": {"read", "list", "piggy_banks", "pagination"}
    },
    
    "bulk_categorize": {
        "description": "Bulk categorize multiple transactions by assigning a category to all of them.",
        "request_model": BulkCategorizeRequest,
        "response_model": TransactionDeleteResponse,
        "core_function": bulk_categorize_transactions,
        "tags": {"write", "bulk", "categorize"}
    },
    
    "bulk_tag": {
        "description": "Bulk tag multiple transactions by assigning one or more tags to all of them.",
        "request_model": BulkTagRequest,
        "response_model": TransactionDeleteResponse,
        "core_function": bulk_tag_transactions,
        "tags": {"write", "bulk", "tag"}
    }
}


def create_transaction_provider():
    """Factory function to create the transaction provider with simplified configuration."""
    return create_provider_from_config(EntityType.TRANSACTION, TRANSACTION_OPERATIONS)

transaction_provider = create_transaction_provider()