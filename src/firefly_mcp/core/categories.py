from firefly_mcp.models.model import CategoryArray, CategorySingle, Category, TransactionArray, AttachmentArray
from firefly_mcp.models.requests import (
    CategoryGetRequest, 
    CategoryListRequest, 
    CategoryUpdateRequest,
    CategoryTransactionsRequest,
    CategoryAttachmentsRequest,
    CategoryDeleteRequest,
    CategoryDeleteResponse
)
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_categories(params: CategoryListRequest) -> CategoryArray:
    """List all categories wrapped in CategoryArray."""
    response = client.get("/categories", params=params.model_dump(exclude_none=True, mode='json'))
    raise_api_error_if_any(response)
    return CategoryArray.model_validate(response.json())


def get_category(request: CategoryGetRequest) -> CategorySingle:
    """Get a single category."""
    params = request.model_dump(exclude_none=True, mode='json')
    category_id = params.pop("id")
    response = client.get(f"/categories/{category_id}", params=params)
    raise_api_error_if_any(response)
    return CategorySingle.model_validate(response.json())


def create_category(request: Category) -> CategorySingle:
    """Create one category."""
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/categories", json=data)
    raise_api_error_if_any(response)
    return CategorySingle.model_validate(response.json())


def update_category(request: CategoryUpdateRequest) -> CategorySingle:
    """Update one category."""
    data = request.model_dump(exclude_none=True, mode='json')
    category_id = data.pop("id")
    category_data = data.pop("category_update")
    response = client.put(f"/categories/{category_id}", json=category_data)
    raise_api_error_if_any(response)
    return CategorySingle.model_validate(response.json())


def delete_category(request: CategoryDeleteRequest) -> CategoryDeleteResponse:
    """Delete one category."""
    category_id = request.id
    response = client.delete(f"/categories/{category_id}")
    raise_api_error_if_any(response)
    return CategoryDeleteResponse(message="Category deleted successfully")


def list_category_transactions(request: CategoryTransactionsRequest) -> TransactionArray:
    """List all transactions in a category."""
    params = request.model_dump(exclude_none=True, mode='json')
    category_id = params.pop("id")
    response = client.get(f"/categories/{category_id}/transactions", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def list_category_attachments(request: CategoryAttachmentsRequest) -> AttachmentArray:
    """List all attachments for a category."""
    params = request.model_dump(exclude_none=True, mode='json')
    category_id = params.pop("id")
    response = client.get(f"/categories/{category_id}/attachments", params=params)
    raise_api_error_if_any(response)
    return AttachmentArray.model_validate(response.json())
