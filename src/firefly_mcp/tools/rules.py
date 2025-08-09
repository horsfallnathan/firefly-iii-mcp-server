"""Rule provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.rules import (
    get_rule, list_rules, create_rule, update_rule, delete_rule,
    test_rule, trigger_rule
)
from firefly_mcp.models.model import (
    RuleArray, RuleSingle, RuleStore, TransactionArray
)
from firefly_mcp.models.requests import (
    RuleGetRequest, RuleListRequest, RuleUpdateRequest,
    RuleTestRequest, RuleTriggerRequest, RuleDeleteRequest, RuleDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
RULE_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all rules. Can be filtered and paginated.",
        "request_model": RuleListRequest,
        "response_model": RuleArray,
        "core_function": list_rules,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific rule by ID.",
        "request_model": RuleGetRequest,
        "response_model": RuleSingle,
        "core_function": get_rule,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new rule.",
        "request_model": RuleStore,
        "response_model": RuleSingle,
        "core_function": create_rule,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing rule.",
        "request_model": RuleUpdateRequest,
        "response_model": RuleSingle,
        "core_function": update_rule,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a rule.",
        "request_model": RuleDeleteRequest,
        "response_model": RuleDeleteResponse,
        "core_function": delete_rule,
        "tags": {"write", "delete"}
    },
    
    "test": {
        "description": "Test which transactions would be hit by the rule. No changes will be made. Can be limited by date range and accounts.",
        "request_model": RuleTestRequest,
        "response_model": TransactionArray,
        "core_function": test_rule,
        "tags": {"read", "test", "simulation"}
    },
    
    "trigger": {
        "description": "Fire the rule on your transactions. Changes will be made by the rule! Can be limited by date range and accounts.",
        "request_model": RuleTriggerRequest,
        "response_model": RuleDeleteResponse,
        "core_function": trigger_rule,
        "tags": {"write", "trigger", "execute"}
    }
}


def create_rule_provider():
    """Factory function to create the rule provider with simplified configuration."""
    return create_provider_from_config(EntityType.RULE, RULE_OPERATIONS)

rule_provider = create_rule_provider()