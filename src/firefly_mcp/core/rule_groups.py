from firefly_mcp.models.model import RuleGroupArray, RuleGroupSingle, RuleGroupStore, RuleArray, TransactionArray
from firefly_mcp.models.requests import (
    RuleGroupGetRequest, 
    RuleGroupListRequest, 
    RuleGroupUpdateRequest,
    RuleGroupListRulesRequest,
    RuleGroupTestRequest,
    RuleGroupTriggerRequest,
    RuleGroupDeleteRequest,
    RuleGroupDeleteResponse
)
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_rule_groups(request: RuleGroupListRequest) -> RuleGroupArray:
    """List all rule groups wrapped in RuleGroupArray.
    
    Args:
        request: RuleGroupListRequest containing pagination options
        
    Returns:
        RuleGroupArray: Array of rule groups
    """
    params = request.model_dump(exclude_none=True, mode='json')
    response = client.get("/v1/rule-groups", params=params)
    raise_api_error_if_any(response)
    return RuleGroupArray.model_validate(response.json())


def get_rule_group(request: RuleGroupGetRequest) -> RuleGroupSingle:
    """Get a single rule group.
    
    Args:
        request: RuleGroupGetRequest containing rule group ID
        
    Returns:
        RuleGroupSingle: Properly typed rule group response
    """
    params = request.model_dump(exclude_none=True, mode='json')
    rule_group_id = params.pop("id")
    response = client.get(f"/v1/rule-groups/{rule_group_id}", params=params)
    raise_api_error_if_any(response)
    return RuleGroupSingle.model_validate(response.json())


def create_rule_group(request: RuleGroupStore) -> RuleGroupSingle:
    """Create one rule group.
    
    Args:
        request: RuleGroupStore containing rule group data
        
    Returns:
        RuleGroupSingle: Properly typed rule group response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/v1/rule-groups", json=data)
    raise_api_error_if_any(response)
    return RuleGroupSingle.model_validate(response.json())


def update_rule_group(request: RuleGroupUpdateRequest) -> RuleGroupSingle:
    """Update one rule group.
    
    Args:
        request: RuleGroupUpdateRequest containing ID and update data
        
    Returns:
        RuleGroupSingle: Properly typed rule group response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    rule_group_id = data.pop("id")
    rule_group_data = data.pop("rule_group_update")
    response = client.put(f"/v1/rule-groups/{rule_group_id}", json=rule_group_data)
    raise_api_error_if_any(response)
    return RuleGroupSingle.model_validate(response.json())


def delete_rule_group(request: RuleGroupDeleteRequest) -> RuleGroupDeleteResponse:
    """Delete one rule group.
    
    Args:
        request: RuleGroupDeleteRequest containing rule group ID
        
    Returns:
        RuleGroupDeleteResponse: Success message
    """
    rule_group_id = request.id
    response = client.delete(f"/v1/rule-groups/{rule_group_id}")
    raise_api_error_if_any(response)
    return RuleGroupDeleteResponse(message="Rule group deleted successfully")


def list_rule_group_rules(request: RuleGroupListRulesRequest) -> RuleArray:
    """List rules in a rule group.
    
    Args:
        request: RuleGroupListRulesRequest containing rule group ID and pagination
        
    Returns:
        RuleArray: Array of rules in the rule group
    """
    params = request.model_dump(exclude_none=True, mode='json')
    rule_group_id = params.pop("id")
    response = client.get(f"/v1/rule-groups/{rule_group_id}/rules", params=params)
    raise_api_error_if_any(response)
    return RuleArray.model_validate(response.json())


def test_rule_group(request: RuleGroupTestRequest) -> TransactionArray:
    """Test which transactions would be hit by the rule group. No changes will be made.
    
    Args:
        request: RuleGroupTestRequest containing rule group ID and test parameters
        
    Returns:
        TransactionArray: Array of transactions that would be affected
    """
    params = request.model_dump(exclude_none=True, mode='json')
    rule_group_id = params.pop("id")
    response = client.get(f"/v1/rule-groups/{rule_group_id}/test", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def trigger_rule_group(request: RuleGroupTriggerRequest) -> RuleGroupDeleteResponse:
    """Fire the rule group on your transactions. Changes will be made by the rules in the rule group.
    
    Args:
        request: RuleGroupTriggerRequest containing rule group ID and trigger parameters
        
    Returns:
        RuleGroupDeleteResponse: Success message (reusing for consistency)
    """
    params = request.model_dump(exclude_none=True, mode='json')
    rule_group_id = params.pop("id")
    response = client.post(f"/v1/rule-groups/{rule_group_id}/trigger", params=params)
    raise_api_error_if_any(response)
    return RuleGroupDeleteResponse(message="Rule group triggered successfully")