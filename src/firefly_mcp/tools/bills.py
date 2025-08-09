"""Bill provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.bills import (
    create_bill, 
    delete_bill, 
    get_bill, 
    list_bills, 
    update_bill,
    list_bill_transactions,
    list_bill_attachments,
    list_bill_rules
)
from firefly_mcp.models.model import (
    BillArray, BillSingle, BillStore, TransactionArray, 
    AttachmentArray, RuleArray
)
from firefly_mcp.models.requests import (
    BillGetRequest, 
    BillListRequest, 
    BillUpdateRequest,
    BillTransactionsRequest,
    BillAttachmentsRequest,
    BillRulesRequest,
    BillDeleteRequest,
    BillDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
BILL_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all bills. Can be filtered and paginated with date ranges to calculate payment and paid dates.",
        "request_model": BillListRequest,
        "response_model": BillArray,
        "core_function": list_bills,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific bill by ID with optional date ranges to calculate payment and paid dates.",
        "request_model": BillGetRequest,
        "response_model": BillSingle,
        "core_function": get_bill,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new bill.",
        "request_model": BillStore,
        "response_model": BillSingle,
        "core_function": create_bill,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing bill.",
        "request_model": BillUpdateRequest,
        "response_model": BillSingle,
        "core_function": update_bill,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a bill.",
        "request_model": BillDeleteRequest,
        "response_model": BillDeleteResponse,
        "core_function": delete_bill,
        "tags": {"write", "delete"}
    },
    
    "list_transactions": {
        "description": "List all transactions associated with a bill, optionally limited to date ranges and transaction types.",
        "request_model": BillTransactionsRequest,
        "response_model": TransactionArray,
        "core_function": list_bill_transactions,
        "tags": {"read", "list", "transactions", "pagination"}
    },
    
    "list_attachments": {
        "description": "List all attachments for a bill.",
        "request_model": BillAttachmentsRequest,
        "response_model": AttachmentArray,
        "core_function": list_bill_attachments,
        "tags": {"read", "list", "attachments", "pagination"}
    },
    
    "list_rules": {
        "description": "List all rules that have an action to set the bill to this bill.",
        "request_model": BillRulesRequest,
        "response_model": RuleArray,
        "core_function": list_bill_rules,
        "tags": {"read", "list", "rules", "pagination"}
    }
}


def create_bill_provider():
    """Factory function to create the bill provider with simplified configuration."""
    return create_provider_from_config(EntityType.BILL, BILL_OPERATIONS)

bill_provider = create_bill_provider()
