"""Budget provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.budgets import (
    create_budget, 
    delete_budget, 
    get_budget, 
    list_budgets, 
    update_budget,
    list_limits,
    get_limit,
    create_limit,
    update_limit,
    delete_limit,
    list_budget_transactions,
    list_budget_attachments,
    list_transactions_without_budget
)
from firefly_mcp.models.model import (
    BudgetArray, BudgetSingle, BudgetStore,
    BudgetLimitArray, BudgetLimitSingle,
    TransactionArray, AttachmentArray
)
from firefly_mcp.models.requests import (
    BudgetGetRequest, 
    BudgetListRequest, 
    BudgetUpdateRequest,
    BudgetLimitsRequest,
    BudgetLimitGetRequest,
    BudgetLimitCreateRequest,
    BudgetLimitUpdateRequest,
    BudgetTransactionsRequest,
    BudgetAttachmentsRequest,
    BudgetTransactionsWithoutBudgetRequest,
    BudgetDeleteRequest,
    BudgetDeleteResponse,
    BudgetLimitDeleteRequest,
    BudgetLimitDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
BUDGET_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all budgets. Can be filtered by date range to include spending info.",
        "request_model": BudgetListRequest,
        "response_model": BudgetArray,
        "core_function": list_budgets,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific budget by ID. Can include spending info for date range.",
        "request_model": BudgetGetRequest,
        "response_model": BudgetSingle,
        "core_function": get_budget,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new budget.",
        "request_model": BudgetStore,
        "response_model": BudgetSingle,
        "core_function": create_budget,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing budget.",
        "request_model": BudgetUpdateRequest,
        "response_model": BudgetSingle,
        "core_function": update_budget,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a budget.",
        "request_model": BudgetDeleteRequest,
        "response_model": BudgetDeleteResponse,
        "core_function": delete_budget,
        "tags": {"write", "delete"}
    },
    
    "list_limits": {
        "description": "List all budget limits for a specific budget with spending info.",
        "request_model": BudgetLimitsRequest,
        "response_model": BudgetLimitArray,
        "core_function": list_limits,
        "tags": {"read", "list", "limits", "pagination"}
    },
    
    "get_limit": {
        "description": "Get details for a specific budget limit by budget ID and limit ID.",
        "request_model": BudgetLimitGetRequest,
        "response_model": BudgetLimitSingle,
        "core_function": get_limit,
        "tags": {"read", "single", "limits"}
    },
    
    "create_limit": {
        "description": "Create a new budget limit.",
        "request_model": BudgetLimitCreateRequest,
        "response_model": BudgetLimitSingle,
        "core_function": create_limit,
        "tags": {"write", "create", "limits"}
    },
    
    "update_limit": {
        "description": "Update an existing budget limit.",
        "request_model": BudgetLimitUpdateRequest,
        "response_model": BudgetLimitSingle,
        "core_function": update_limit,
        "tags": {"write", "update", "limits"}
    },
    
    "delete_limit": {
        "description": "Delete a budget limit.",
        "request_model": BudgetLimitDeleteRequest,
        "response_model": BudgetLimitDeleteResponse,
        "core_function": delete_limit,
        "tags": {"write", "delete", "limits"}
    },
    
    "list_transactions": {
        "description": "List all transactions for a specific budget with optional date and type filters.",
        "request_model": BudgetTransactionsRequest,
        "response_model": TransactionArray,
        "core_function": list_budget_transactions,
        "tags": {"read", "list", "transactions", "pagination"}
    },
    
    "list_attachments": {
        "description": "List all attachments for a specific budget.",
        "request_model": BudgetAttachmentsRequest,
        "response_model": AttachmentArray,
        "core_function": list_budget_attachments,
        "tags": {"read", "list", "attachments", "pagination"}
    },
    
    "list_transactions_without_budget": {
        "description": "List all transactions that are not linked to any budget.",
        "request_model": BudgetTransactionsWithoutBudgetRequest,
        "response_model": TransactionArray,
        "core_function": list_transactions_without_budget,
        "tags": {"read", "list", "transactions", "pagination", "unlinked"}
    }
}


def create_budget_provider():
    """Factory function to create the budget provider with simplified configuration."""
    return create_provider_from_config(EntityType.BUDGET, BUDGET_OPERATIONS)

budget_provider = create_budget_provider()
