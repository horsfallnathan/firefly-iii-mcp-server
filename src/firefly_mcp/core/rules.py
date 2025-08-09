from firefly_mcp.models.model import RuleArray, RuleSingle, RuleStore, TransactionArray
from firefly_mcp.models.requests import (
    RuleGetRequest, 
    RuleListRequest, 
    RuleUpdateRequest,
    RuleTestRequest,
    RuleTriggerRequest,
    RuleDeleteRequest,
    RuleDeleteResponse
)
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_rules(request: RuleListRequest) -> RuleArray:
    """List all rules wrapped in RuleArray.
    
    Args:
        request: RuleListRequest containing pagination options
        
    Returns:
        RuleArray: Array of rules
    """
    params = request.model_dump(exclude_none=True, mode='json')
    response = client.get("/v1/rules", params=params)
    raise_api_error_if_any(response)
    return RuleArray.model_validate(response.json())


def get_rule(request: RuleGetRequest) -> RuleSingle:
    """Get a single rule.
    
    Args:
        request: RuleGetRequest containing rule ID
        
    Returns:
        RuleSingle: Properly typed rule response
    """
    params = request.model_dump(exclude_none=True, mode='json')
    rule_id = params.pop("id")
    response = client.get(f"/v1/rules/{rule_id}", params=params)
    raise_api_error_if_any(response)
    return RuleSingle.model_validate(response.json())


def create_rule(request: RuleStore) -> RuleSingle:
    """Create one rule.
    
    Args:
        request: RuleStore containing rule data
        
    Returns:
        RuleSingle: Properly typed rule response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/v1/rules", json=data)
    raise_api_error_if_any(response)
    return RuleSingle.model_validate(response.json())


def update_rule(request: RuleUpdateRequest) -> RuleSingle:
    """Update one rule.
    
    Args:
        request: RuleUpdateRequest containing ID and update data
        
    Returns:
        RuleSingle: Properly typed rule response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    rule_id = data.pop("id")
    rule_data = data.pop("rule_update")
    response = client.put(f"/v1/rules/{rule_id}", json=rule_data)
    raise_api_error_if_any(response)
    return RuleSingle.model_validate(response.json())


def delete_rule(request: RuleDeleteRequest) -> RuleDeleteResponse:
    """Delete one rule.
    
    Args:
        request: RuleDeleteRequest containing rule ID
        
    Returns:
        RuleDeleteResponse: Success message
    """
    rule_id = request.id
    response = client.delete(f"/v1/rules/{rule_id}")
    raise_api_error_if_any(response)
    return RuleDeleteResponse(message="Rule deleted successfully")


def test_rule(request: RuleTestRequest) -> TransactionArray:
    """Test which transactions would be hit by the rule. No changes will be made.
    
    Args:
        request: RuleTestRequest containing rule ID and test parameters
        
    Returns:
        TransactionArray: Array of transactions that would be affected
    """
    params = request.model_dump(exclude_none=True, mode='json')
    rule_id = params.pop("id")
    response = client.get(f"/v1/rules/{rule_id}/test", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def trigger_rule(request: RuleTriggerRequest) -> RuleDeleteResponse:
    """Fire the rule on your transactions. Changes will be made by the rule.
    
    Args:
        request: RuleTriggerRequest containing rule ID and trigger parameters
        
    Returns:
        RuleDeleteResponse: Success message (reusing for consistency)
    """
    params = request.model_dump(exclude_none=True, mode='json')
    rule_id = params.pop("id")
    response = client.post(f"/v1/rules/{rule_id}/trigger", params=params)
    raise_api_error_if_any(response)
    return RuleDeleteResponse(message="Rule triggered successfully")