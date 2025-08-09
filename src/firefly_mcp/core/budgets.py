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
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_budgets(params: BudgetListRequest) -> BudgetArray:
    """List all budgets wrapped in BudgetArray."""
    response = client.get("/budgets", params=params.model_dump(exclude_none=True, mode='json'))
    raise_api_error_if_any(response)
    return BudgetArray.model_validate(response.json())


def get_budget(request: BudgetGetRequest) -> BudgetSingle:
    """Get a single budget."""
    params = request.model_dump(exclude_none=True, mode='json')
    budget_id = params.pop("id")
    response = client.get(f"/budgets/{budget_id}?", params=params)
    raise_api_error_if_any(response)
    return BudgetSingle.model_validate(response.json())


def create_budget(request: BudgetStore) -> BudgetSingle:
    """Create one budget."""
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/budgets", json=data)
    raise_api_error_if_any(response)
    return BudgetSingle.model_validate(response.json())


def update_budget(request: BudgetUpdateRequest) -> BudgetSingle:
    """Update one budget."""
    data = request.model_dump(exclude_none=True, mode='json')
    budget_id = data.pop("id")
    # Extract the budget_update data
    budget_update_data = data.pop("budget_update")
    response = client.put(f"/budgets/{budget_id}", json=budget_update_data)
    raise_api_error_if_any(response)
    return BudgetSingle.model_validate(response.json())


def delete_budget(request: BudgetDeleteRequest) -> BudgetDeleteResponse:
    """Delete one budget."""
    budget_id = request.id
    response = client.delete(f"/budgets/{budget_id}")
    raise_api_error_if_any(response)
    return BudgetDeleteResponse(message="Budget deleted successfully")


def list_limits(request: BudgetLimitsRequest) -> BudgetLimitArray:
    """List all budget limits for a specific budget."""
    params = request.model_dump(exclude_none=True, mode='json')
    budget_id = params.pop("id")
    response = client.get(f"/budgets/{budget_id}/limits", params=params)
    raise_api_error_if_any(response)
    return BudgetLimitArray.model_validate(response.json())


def get_limit(request: BudgetLimitGetRequest) -> BudgetLimitSingle:
    """Get a single budget limit."""
    params = request.model_dump(exclude_none=True, mode='json')
    budget_id = params.pop("budget_id")
    limit_id = params.pop("limit_id")
    response = client.get(f"/budgets/{budget_id}/limits/{limit_id}", params=params)
    raise_api_error_if_any(response)
    return BudgetLimitSingle.model_validate(response.json())


def create_limit(request: BudgetLimitCreateRequest) -> BudgetLimitSingle:
    """Create one budget limit."""
    data = request.model_dump(exclude_none=True, mode='json')
    budget_id = data.pop("budget_id")
    # Extract the budget_limit_store data
    budget_limit_data = data.pop("budget_limit_store")
    response = client.post(f"/budgets/{budget_id}/limits", json=budget_limit_data)
    raise_api_error_if_any(response)
    return BudgetLimitSingle.model_validate(response.json())


def update_limit(request: BudgetLimitUpdateRequest) -> BudgetLimitSingle:
    """Update one budget limit."""
    data = request.model_dump(exclude_none=True, mode='json')
    budget_id = data.pop("budget_id")
    limit_id = data.pop("limit_id")
    # Extract the budget_limit data
    budget_limit_data = data.pop("budget_limit")
    response = client.put(f"/budgets/{budget_id}/limits/{limit_id}", json=budget_limit_data)
    raise_api_error_if_any(response)
    return BudgetLimitSingle.model_validate(response.json())


def delete_limit(request: BudgetLimitDeleteRequest) -> BudgetLimitDeleteResponse:
    """Delete one budget limit."""
    budget_id = request.budget_id
    limit_id = request.limit_id
    response = client.delete(f"/budgets/{budget_id}/limits/{limit_id}")
    raise_api_error_if_any(response)
    return BudgetLimitDeleteResponse(message="Budget limit deleted successfully")


def list_budget_transactions(request: BudgetTransactionsRequest) -> TransactionArray:
    """List all transactions for a specific budget."""
    params = request.model_dump(exclude_none=True, mode='json')
    budget_id = params.pop("id")
    response = client.get(f"/budgets/{budget_id}/transactions", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def list_budget_attachments(request: BudgetAttachmentsRequest) -> AttachmentArray:
    """List all attachments for a specific budget."""
    params = request.model_dump(exclude_none=True, mode='json')
    budget_id = params.pop("id")
    response = client.get(f"/budgets/{budget_id}/attachments", params=params)
    raise_api_error_if_any(response)
    return AttachmentArray.model_validate(response.json())


def list_transactions_without_budget(request: BudgetTransactionsWithoutBudgetRequest) -> TransactionArray:
    """List all transactions not linked to any budget."""
    params = request.model_dump(exclude_none=True, mode='json')
    response = client.get("/budgets/transactions-without-budget", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())
