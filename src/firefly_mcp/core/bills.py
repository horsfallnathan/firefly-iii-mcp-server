from firefly_mcp.models.model import BillArray, BillSingle, BillStore, TransactionArray, AttachmentArray, RuleArray
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
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_bills(params: BillListRequest) -> BillArray:
    """List all bills wrapped in BillArray."""
    response = client.get("/bills", params=params.model_dump(exclude_none=True, mode='json'))
    raise_api_error_if_any(response)
    return BillArray.model_validate(response.json())


def get_bill(request: BillGetRequest) -> BillSingle:
    """Get a single bill."""
    params = request.model_dump(exclude_none=True, mode='json')
    bill_id = params.pop("id")
    response = client.get(f"/bills/{bill_id}", params=params)
    raise_api_error_if_any(response)
    return BillSingle.model_validate(response.json())


def create_bill(request: BillStore) -> BillSingle:
    """Create one bill."""
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/bills", json=data)
    raise_api_error_if_any(response)
    return BillSingle.model_validate(response.json())


def update_bill(request: BillUpdateRequest) -> BillSingle:
    """Update one bill."""
    data = request.model_dump(exclude_none=True, mode='json')
    bill_id = data.pop("id")
    bill_data = data.pop("bill_update")
    response = client.put(f"/bills/{bill_id}", json=bill_data)
    raise_api_error_if_any(response)
    return BillSingle.model_validate(response.json())


def delete_bill(request: BillDeleteRequest) -> BillDeleteResponse:
    """Delete one bill."""
    bill_id = request.id
    response = client.delete(f"/bills/{bill_id}")
    raise_api_error_if_any(response)
    return BillDeleteResponse(message="Bill deleted successfully")


def list_bill_transactions(request: BillTransactionsRequest) -> TransactionArray:
    """List all transactions associated with a bill."""
    params = request.model_dump(exclude_none=True, mode='json')
    bill_id = params.pop("id")
    response = client.get(f"/bills/{bill_id}/transactions", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def list_bill_attachments(request: BillAttachmentsRequest) -> AttachmentArray:
    """List all attachments for a bill."""
    params = request.model_dump(exclude_none=True, mode='json')
    bill_id = params.pop("id")
    response = client.get(f"/bills/{bill_id}/attachments", params=params)
    raise_api_error_if_any(response)
    return AttachmentArray.model_validate(response.json())


def list_bill_rules(request: BillRulesRequest) -> RuleArray:
    """List all rules associated with a bill."""
    params = request.model_dump(exclude_none=True, mode='json')
    bill_id = params.pop("id")
    response = client.get(f"/bills/{bill_id}/rules", params=params)
    raise_api_error_if_any(response)
    return RuleArray.model_validate(response.json())
