
from firefly_mcp.models.model import AccountArray, AccountSingle, AccountStore, TransactionArray, AttachmentArray, PiggyBankArray
from firefly_mcp.models.requests import AccountDeleteRequest, AccountDeleteResponse, AccountGetRequest, AccountListRequest, AccountUpdateRequest, AccountTransactionsRequest, AccountAttachmentsRequest, AccountPiggyBanksRequest
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_accounts(request: AccountListRequest) -> AccountArray:
    """List all accounts wrapped in AccountArray.
    
    Args:
        account_type: Optional filter by account type.
        limit: Pagination limit.
        page: Page number.
        date: Balance date.
    """
    params = request.model_dump(exclude_none=True, mode='json')
    response = client.get("/accounts", params=params)
    raise_api_error_if_any(response)
    return AccountArray.model_validate(response.json())

def get_account(request: AccountGetRequest) -> AccountSingle:
    """Get a single account. Can include balance on specific date.
    
    Returns:
        AccountSingle: Properly typed account response.
    """

    params = request.model_dump(exclude_none=True, mode='json')
    account_id = params.pop("id")
    response = client.get(f"/accounts/{account_id}", params=params)
    raise_api_error_if_any(response)
    return AccountSingle.model_validate(response.json())

def create_account(request: AccountStore) -> AccountSingle:
    """Create one account.
    
    Args:
        request: AccountStore containing account data
        
    Returns:
        AccountSingle: Properly typed account response.
    """
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/accounts", json=data)
    raise_api_error_if_any(response)
    return AccountSingle.model_validate(response.json())
    

def update_account(request: AccountUpdateRequest) -> AccountSingle:
    """Update one account.
    
    Args:
        request: AccountUpdateRequest containing ID and update data
        
    Returns:
        AccountSingle: Properly typed account response.
    """
    data = request.model_dump(exclude_none=True, mode='json')
    account_id = data.pop("id")
    response = client.put(f"/accounts/{account_id}", json=data.get("account_update", {}))
    raise_api_error_if_any(response)
    return AccountSingle.model_validate(response.json())


def delete_account(
    request: AccountDeleteRequest
) -> AccountDeleteResponse:
    """Delete one account.
    
    Args:
        id: ID of the account to delete
        
    Returns:
        str: Success message
    """
    account_id = request.id
    response = client.delete(f"/accounts/{account_id}")
    raise_api_error_if_any(response)
    return AccountDeleteResponse(message="Account deleted successfully")


def list_account_transactions(request: AccountTransactionsRequest) -> TransactionArray:
    """List all transactions for a specific account.
    
    Args:
        request: AccountTransactionsRequest containing account ID and optional filters
        
    Returns:
        TransactionArray: Array of transactions for the account
    """
    params = request.model_dump(exclude_none=True, mode='json')
    account_id = params.pop("id")
    response = client.get(f"/accounts/{account_id}/transactions", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def list_account_attachments(request: AccountAttachmentsRequest) -> AttachmentArray:
    """List all attachments for a specific account.
    
    Args:
        request: AccountAttachmentsRequest containing account ID and pagination
        
    Returns:
        AttachmentArray: Array of attachments for the account
    """
    params = request.model_dump(exclude_none=True, mode='json')
    account_id = params.pop("id")
    response = client.get(f"/accounts/{account_id}/attachments", params=params)
    raise_api_error_if_any(response)
    return AttachmentArray.model_validate(response.json())


def list_account_piggy_banks(request: AccountPiggyBanksRequest) -> PiggyBankArray:
    """List all piggy banks for a specific account.
    
    Args:
        request: AccountPiggyBanksRequest containing account ID and pagination
        
    Returns:
        PiggyBankArray: Array of piggy banks for the account
    """
    params = request.model_dump(exclude_none=True, mode='json')
    account_id = params.pop("id")
    response = client.get(f"/accounts/{account_id}/piggy-banks", params=params)
    raise_api_error_if_any(response)
    return PiggyBankArray.model_validate(response.json())