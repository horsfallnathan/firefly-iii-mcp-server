"""Rule group provider.
"""

import logging
from typing import Dict, Any

from firefly_mcp.core.rule_groups import (
    get_rule_group, list_rule_groups, create_rule_group, update_rule_group, delete_rule_group,
    list_rule_group_rules, test_rule_group, trigger_rule_group
)
from firefly_mcp.models.model import (
    RuleGroupArray, RuleGroupSingle, RuleGroupStore, RuleArray, TransactionArray
)
from firefly_mcp.models.requests import (
    RuleGroupGetRequest, RuleGroupListRequest, RuleGroupUpdateRequest,
    RuleGroupListRulesRequest, RuleGroupTestRequest, RuleGroupTriggerRequest,
    RuleGroupDeleteRequest, RuleGroupDeleteResponse
)
from firefly_mcp.tools.registry import EntityType, create_provider_from_config

logger = logging.getLogger(__name__)


# Operation definitions
RULE_GROUP_OPERATIONS: Dict[str, Dict[str, Any]] = {
    "list": {
        "description": "List all rule groups. Can be filtered and paginated.",
        "request_model": RuleGroupListRequest,
        "response_model": RuleGroupArray,
        "core_function": list_rule_groups,
        "tags": {"read", "list", "pagination"}
    },
    
    "get": {
        "description": "Get details for a specific rule group by ID.",
        "request_model": RuleGroupGetRequest,
        "response_model": RuleGroupSingle,
        "core_function": get_rule_group,
        "tags": {"read", "single"}
    },
    
    "create": {
        "description": "Create a new rule group.",
        "request_model": RuleGroupStore,
        "response_model": RuleGroupSingle,
        "core_function": create_rule_group,
        "tags": {"write", "create"}
    },
    
    "update": {
        "description": "Update an existing rule group.",
        "request_model": RuleGroupUpdateRequest,
        "response_model": RuleGroupSingle,
        "core_function": update_rule_group,
        "tags": {"write", "update"}
    },
    
    "delete": {
        "description": "Delete a rule group.",
        "request_model": RuleGroupDeleteRequest,
        "response_model": RuleGroupDeleteResponse,
        "core_function": delete_rule_group,
        "tags": {"write", "delete"}
    },
    
    "list_rules": {
        "description": "List rules in a specific rule group. Can be paginated.",
        "request_model": RuleGroupListRulesRequest,
        "response_model": RuleArray,
        "core_function": list_rule_group_rules,
        "tags": {"read", "list", "rules", "pagination"}
    },
    
    "test": {
        "description": "Test which transactions would be hit by the rule group. No changes will be made. Can be limited by date range, search limits, and accounts.",
        "request_model": RuleGroupTestRequest,
        "response_model": TransactionArray,
        "core_function": test_rule_group,
        "tags": {"read", "test", "simulation"}
    },
    
    "trigger": {
        "description": "Fire the rule group on your transactions. Changes will be made by the rules in the rule group! Can be limited by date range and accounts.",
        "request_model": RuleGroupTriggerRequest,
        "response_model": RuleGroupDeleteResponse,
        "core_function": trigger_rule_group,
        "tags": {"write", "trigger", "execute"}
    }
}


def create_rule_group_provider():
    """Factory function to create the rule group provider with simplified configuration."""
    return create_provider_from_config(EntityType.RULE_GROUP, RULE_GROUP_OPERATIONS)

rule_group_provider = create_rule_group_provider()