from firefly_mcp.models.model import TransactionArray, TransactionSingle, TransactionStore, AttachmentArray, PiggyBankEventArray
from firefly_mcp.models.requests import (
    TransactionGetRequest, 
    TransactionListRequest, 
    TransactionUpdateRequest, 
    TransactionAttachmentsRequest, 
    TransactionPiggyBankEventsRequest,
    TransactionDeleteRequest,
    TransactionDeleteResponse,
    BulkCategorizeRequest,
    BulkTagRequest
)
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_transactions(request: TransactionListRequest) -> TransactionArray:
    """List all transactions wrapped in TransactionArray.
    
    Args:
        request: TransactionListRequest containing filters and pagination
        
    Returns:
        TransactionArray: Array of transactions
    """
    params = request.model_dump(exclude_none=True, mode='json')
    response = client.get("/transactions", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def get_transaction(request: TransactionGetRequest) -> TransactionSingle:
    """Get a single transaction.
    
    Args:
        request: TransactionGetRequest containing transaction ID
        
    Returns:
        TransactionSingle: Properly typed transaction response
    """
    params = request.model_dump(exclude_none=True, mode='json')
    transaction_id = params.pop("id")
    response = client.get(f"/transactions/{transaction_id}", params=params)
    raise_api_error_if_any(response)
    return TransactionSingle.model_validate(response.json())


def create_transaction(request: TransactionStore) -> TransactionSingle:
    """Create one transaction.
    
    Args:
        request: TransactionStore containing transaction data
        
    Returns:
        TransactionSingle: Properly typed transaction response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/transactions", json=data)
    raise_api_error_if_any(response)
    return TransactionSingle.model_validate(response.json())


def update_transaction(request: TransactionUpdateRequest) -> TransactionSingle:
    """Update one transaction.
    
    Args:
        request: TransactionUpdateRequest containing ID and update data
        
    Returns:
        TransactionSingle: Properly typed transaction response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    transaction_id = data.pop("id")
    response = client.put(f"/transactions/{transaction_id}", json=data)
    raise_api_error_if_any(response)
    return TransactionSingle.model_validate(response.json())


def delete_transaction(request: TransactionDeleteRequest) -> TransactionDeleteResponse:
    """Delete one transaction.
    
    Args:
        request: TransactionDeleteRequest containing transaction ID
        
    Returns:
        TransactionDeleteResponse: Success message
    """
    transaction_id = request.id
    response = client.delete(f"/transactions/{transaction_id}")
    raise_api_error_if_any(response)
    return TransactionDeleteResponse(message="Transaction deleted successfully")


def list_transaction_attachments(request: TransactionAttachmentsRequest) -> AttachmentArray:
    """List all attachments for a specific transaction.
    
    Args:
        request: TransactionAttachmentsRequest containing transaction ID and pagination
        
    Returns:
        AttachmentArray: Array of attachments for the transaction
    """
    params = request.model_dump(exclude_none=True, mode='json')
    transaction_id = params.pop("id")
    response = client.get(f"/transactions/{transaction_id}/attachments", params=params)
    raise_api_error_if_any(response)
    return AttachmentArray.model_validate(response.json())


def list_transaction_piggy_bank_events(request: TransactionPiggyBankEventsRequest) -> PiggyBankEventArray:
    """List all piggy bank events for a specific transaction.
    
    Args:
        request: TransactionPiggyBankEventsRequest containing transaction ID and pagination
        
    Returns:
        PiggyBankEventArray: Array of piggy bank events for the transaction
    """
    params = request.model_dump(exclude_none=True, mode='json')
    transaction_id = params.pop("id")
    response = client.get(f"/transactions/{transaction_id}/piggy-bank-events", params=params)
    raise_api_error_if_any(response)
    return PiggyBankEventArray.model_validate(response.json())


def bulk_categorize_transactions(request: BulkCategorizeRequest) -> TransactionDeleteResponse:
    """Bulk categorize multiple transactions.
    
    Args:
        request: BulkCategorizeRequest containing transaction IDs and category name
        
    Returns:
        TransactionDeleteResponse: Success message (reusing for consistency)
    """
    # Use the bulk API endpoint with proper query format
    response = client.post(
        "/data/bulk/transactions",
        params={"query": f"category_name={request.category_name}"},
        json={"transaction_ids": request.transaction_ids}
    )
    raise_api_error_if_any(response)
    return TransactionDeleteResponse(message="Transactions categorized successfully")


def bulk_tag_transactions(request: BulkTagRequest) -> TransactionDeleteResponse:
    """Bulk tag multiple transactions.
    
    Args:
        request: BulkTagRequest containing transaction IDs and tag names
        
    Returns:
        TransactionDeleteResponse: Success message (reusing for consistency)
    """
    # Use the bulk API endpoint with proper query format
    response = client.post(
        "/data/bulk/transactions",
        params={"query": f"tags={','.join(request.tag_names)}"},
        json={"transaction_ids": request.transaction_ids}
    )
    raise_api_error_if_any(response)
    return TransactionDeleteResponse(message="Transactions tagged successfully")