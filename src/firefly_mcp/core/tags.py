from firefly_mcp.models.model import TagArray, TagSingle, TagModelStore, TransactionArray, AttachmentArray
from firefly_mcp.models.requests import (
    TagGetRequest, 
    TagListRequest, 
    TagUpdateRequest,
    TagTransactionsRequest,
    TagAttachmentsRequest,
    TagDeleteRequest,
    TagDeleteResponse
)
from firefly_mcp.lib.http_client import client
from firefly_mcp.lib.exceptions import raise_api_error_if_any


def list_tags(request: TagListRequest) -> TagArray:
    """List all tags wrapped in TagArray.
    
    Args:
        request: TagListRequest containing pagination options
        
    Returns:
        TagArray: Array of tags
    """
    params = request.model_dump(exclude_none=True, mode='json')
    response = client.get("/tags", params=params)
    raise_api_error_if_any(response)
    return TagArray.model_validate(response.json())


def get_tag(request: TagGetRequest) -> TagSingle:
    """Get a single tag.
    
    Args:
        request: TagGetRequest containing tag ID
        
    Returns:
        TagSingle: Properly typed tag response
    """
    params = request.model_dump(exclude_none=True, mode='json')
    tag_id = params.pop("id")
    response = client.get(f"/tags/{tag_id}", params=params)
    raise_api_error_if_any(response)
    return TagSingle.model_validate(response.json())


def create_tag(request: TagModelStore) -> TagSingle:
    """Create one tag.
    
    Args:
        request: TagModelStore containing tag data
        
    Returns:
        TagSingle: Properly typed tag response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    response = client.post("/tags", json=data)
    raise_api_error_if_any(response)
    return TagSingle.model_validate(response.json())


def update_tag(request: TagUpdateRequest) -> TagSingle:
    """Update one tag.
    
    Args:
        request: TagUpdateRequest containing ID and update data
        
    Returns:
        TagSingle: Properly typed tag response
    """
    data = request.model_dump(exclude_none=True, mode='json')
    tag_id = data.pop("id")
    tag_data = data.pop("tag_update")
    response = client.put(f"/tags/{tag_id}", json=tag_data)
    raise_api_error_if_any(response)
    return TagSingle.model_validate(response.json())


def delete_tag(request: TagDeleteRequest) -> TagDeleteResponse:
    """Delete one tag.
    
    Args:
        request: TagDeleteRequest containing tag ID
        
    Returns:
        TagDeleteResponse: Success message
    """
    tag_id = request.id
    response = client.delete(f"/tags/{tag_id}")
    raise_api_error_if_any(response)
    return TagDeleteResponse(message="Tag deleted successfully")


def list_tag_transactions(request: TagTransactionsRequest) -> TransactionArray:
    """List all transactions for a tag.
    
    Args:
        request: TagTransactionsRequest containing tag ID and optional filters
        
    Returns:
        TransactionArray: Array of transactions for the tag
    """
    params = request.model_dump(exclude_none=True, mode='json')
    tag_id = params.pop("id")
    response = client.get(f"/tags/{tag_id}/transactions", params=params)
    raise_api_error_if_any(response)
    return TransactionArray.model_validate(response.json())


def list_tag_attachments(request: TagAttachmentsRequest) -> AttachmentArray:
    """List all attachments for a tag.
    
    Args:
        request: TagAttachmentsRequest containing tag ID and pagination
        
    Returns:
        AttachmentArray: Array of attachments for the tag
    """
    params = request.model_dump(exclude_none=True, mode='json')
    tag_id = params.pop("id")
    response = client.get(f"/tags/{tag_id}/attachments", params=params)
    raise_api_error_if_any(response)
    return AttachmentArray.model_validate(response.json())