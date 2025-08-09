"""Account provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.accounts import (
    get_account, list_accounts, create_account, update_account, delete_account,
    list_account_transactions, list_account_attachments, list_account_piggy_banks
)
from firefly_mcp.models.model import (
    AccountArray, AccountSingle, AccountStore, TransactionArray, 
    AttachmentArray, PiggyBankArray
)
from firefly_mcp.models.requests import (
    AccountGetRequest, AccountListRequest, AccountUpdateRequest,
    AccountTransactionsRequest, AccountAttachmentsRequest, AccountPiggyBanksRequest,
    AccountDeleteRequest, AccountDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
ACCOUNT_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all accounts. Can be filtered by type, paginated, and include balance on specific date.",
        "request_model": AccountListRequest,
        "response_model": AccountArray,
        "core_function": list_accounts,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific account by ID.",
        "request_model": AccountGetRequest,
        "response_model": AccountSingle,
        "core_function": get_account,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new account.",
        "request_model": AccountStore,
        "response_model": AccountSingle,
        "core_function": create_account,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing account.",
        "request_model": AccountUpdateRequest,
        "response_model": AccountSingle,
        "core_function": update_account,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete an account.",
        "request_model": AccountDeleteRequest,
        "response_model": AccountDeleteResponse,
        "core_function": delete_account,
        "tags": {"write", "delete"}
    },
    
    "list_transactions": {
        "description": "List all transactions for a specific account with optional date and type filters.",
        "request_model": AccountTransactionsRequest,
        "response_model": TransactionArray,
        "core_function": list_account_transactions,
        "tags": {"read", "list", "transactions", "pagination"}
    },
    
    "list_attachments": {
        "description": "List all attachments for a specific account.",
        "request_model": AccountAttachmentsRequest,
        "response_model": AttachmentArray,
        "core_function": list_account_attachments,
        "tags": {"read", "list", "attachments", "pagination"}
    },
    
    "list_piggy_banks": {
        "description": "List all piggy banks for a specific account.",
        "request_model": AccountPiggyBanksRequest,
        "response_model": PiggyBankArray,
        "core_function": list_account_piggy_banks,
        "tags": {"read", "list", "piggy_banks", "pagination"}
    }
}


def create_account_provider():
    """Factory function to create the account provider with simplified configuration."""
    return create_provider_from_config(EntityType.ACCOUNT, ACCOUNT_OPERATIONS)

account_provider = create_account_provider()