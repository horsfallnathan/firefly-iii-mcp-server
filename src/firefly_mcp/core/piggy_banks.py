from firefly_mcp.models.model import PiggyBankArray, PiggyBankSingle, PiggyBankStore, PiggyBankEventArray, AttachmentArray
from firefly_mcp.models.requests import (
    PiggyBankGetRequest, 
    PiggyBankListRequest, 
    PiggyBankUpdateRequest,
    PiggyBankEventsRequest,
    PiggyBankAttachmentsRequest,
    PiggyBankDeleteRequest,
    PiggyBankDeleteResponse
)
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_piggy_banks(params: PiggyBankListRequest) -> PiggyBankArray:
    """List all piggy banks wrapped in PiggyBankArray."""
    response = client.get("/piggy-banks", params=params.model_dump(exclude_none=True, mode='json'))
    raise_api_error_if_any(response)
    return PiggyBankArray.model_validate(response.json())


def get_piggy_bank(request: PiggyBankGetRequest) -> PiggyBankSingle:
    """Get a single piggy bank."""
    params = request.model_dump(exclude_none=True, mode='json')
    piggy_bank_id = params.pop("id")
    response = client.get(f"/piggy-banks/{piggy_bank_id}", params=params)
    raise_api_error_if_any(response)
    return PiggyBankSingle.model_validate(response.json())


def create_piggy_bank(request: PiggyBankStore) -> PiggyBankSingle:
    """Create one piggy bank."""
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/piggy-banks", json=data)
    raise_api_error_if_any(response)
    return PiggyBankSingle.model_validate(response.json())


def update_piggy_bank(request: PiggyBankUpdateRequest) -> PiggyBankSingle:
    """Update one piggy bank."""
    data = request.model_dump(exclude_none=True, mode='json')
    piggy_bank_id = data.pop("id")
    piggy_bank_data = data.pop("piggy_bank_update")
    response = client.put(f"/piggy-banks/{piggy_bank_id}", json=piggy_bank_data)
    raise_api_error_if_any(response)
    return PiggyBankSingle.model_validate(response.json())


def delete_piggy_bank(request: PiggyBankDeleteRequest) -> PiggyBankDeleteResponse:
    """Delete one piggy bank."""
    piggy_bank_id = request.id
    response = client.delete(f"/piggy-banks/{piggy_bank_id}")
    raise_api_error_if_any(response)
    return PiggyBankDeleteResponse(message="Piggy bank deleted successfully")


def list_piggy_bank_events(request: PiggyBankEventsRequest) -> PiggyBankEventArray:
    """List all events linked to a piggy bank (adding and removing money)."""
    params = request.model_dump(exclude_none=True, mode='json')
    piggy_bank_id = params.pop("id")
    response = client.get(f"/piggy-banks/{piggy_bank_id}/events", params=params)
    raise_api_error_if_any(response)
    return PiggyBankEventArray.model_validate(response.json())


def list_piggy_bank_attachments(request: PiggyBankAttachmentsRequest) -> AttachmentArray:
    """List all attachments for a piggy bank."""
    params = request.model_dump(exclude_none=True, mode='json')
    piggy_bank_id = params.pop("id")
    response = client.get(f"/piggy-banks/{piggy_bank_id}/attachments", params=params)
    raise_api_error_if_any(response)
    return AttachmentArray.model_validate(response.json())
